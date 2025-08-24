import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_json_from_response(response_text: str) -> str:
    """Extract JSON content from markdown code blocks or clean up the response"""
    # Remove markdown code blocks if present
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    
    # If no code blocks, try to find JSON content
    json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    
    # If still no match, return the original text
    return response_text

def detect_language(code_content):
    """
    Detect the programming language of the code snippet using LLM.
    Returns the detected language as a string.
    """
    code_text = "\n".join(code_content)
    
    prompt = f"""
    Analyze the following code and determine the programming language.
    
    Code:
    {code_text}
    
    Return ONLY the language name in lowercase (e.g., "python", "javascript", "java", "cpp", "csharp", "go", "rust").
    Do not include any other text, just the language name.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a programming language detection expert. Respond with only the language name in lowercase."},
                {"role": "user", "content": prompt},
            ],
            temperature=0
        )
        
        detected_language = response.choices[0].message.content.strip().lower()
        
        # Clean up the response to ensure it's just a language name
        detected_language = re.sub(r'[^a-zA-Z#+]', '', detected_language)
        
        # Handle special cases
        if detected_language in ['c', 'cpp', 'cplusplus']:
            detected_language = 'cpp'
        elif detected_language in ['csharp', 'cs']:
            detected_language = 'csharp'
        
        return detected_language
    except Exception as e:
        # Fallback to a simple heuristic if LLM fails
        code_text_lower = code_text.lower()
        if 'def ' in code_text_lower or 'import ' in code_text_lower or 'print(' in code_text_lower:
            return 'python'
        elif 'function ' in code_text_lower or 'const ' in code_text_lower or 'let ' in code_text_lower:
            return 'javascript'
        elif 'public class' in code_text_lower or 'public static void' in code_text_lower:
            return 'java'
        elif '#include' in code_text_lower or 'std::' in code_text_lower:
            return 'cpp'
        elif 'using System;' in code_text_lower or 'namespace ' in code_text_lower:
            return 'csharp'
        elif 'package ' in code_text_lower or 'import (' in code_text_lower:
            return 'go'
        elif 'fn ' in code_text_lower or 'let ' in code_text_lower or 'use ' in code_text_lower:
            return 'rust'
        else:
            return 'unknown'

def review_snippet(snippet):
    """
    Sends a code snippet to the LLM for review.
    First detects the language, then performs the review.
    Returns summary, line-specific buggy comments, and overall quality.
    """
    
    # Detect language first
    detected_language = detect_language(snippet["content"])
    
    # Update the snippet with detected language
    snippet["language"] = detected_language
    
    code_text = "\n".join(
        f"{i+1}: {line}" for i, line in enumerate(snippet["content"])
    )

    prompt = f"""
    You are a {detected_language} code reviewer. Analyze the following code:

    Filename: {snippet["filename"]}
    Language: {detected_language}
    Code:
    {code_text}

    Please return the result in strict JSON format with the following fields:
    - summary: a brief quality summary
    - line_comments: an object mapping line numbers to comments (ONLY for buggy lines)
    - quality: one of ["Good", "Needs Improvement", "Buggy"]
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are an expert {detected_language} code reviewer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0
    )

    review_text = response.choices[0].message.content

    try:
        # Extract JSON content from the response
        json_content = extract_json_from_response(review_text)
        review_data = json.loads(json_content)
    except Exception as e:
        review_data = {
            "summary": "LLM response could not be parsed.",
            "line_comments": {},
            "quality": "Needs Improvement"
        }

    return review_data
