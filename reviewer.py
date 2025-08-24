import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
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

def review_snippet(snippet):
    """
    Sends a code snippet to the LLM for review.
    Returns summary, line-specific buggy comments, and overall quality.
    """

    code_text = "\n".join(
        f"{i+1}: {line}" for i, line in enumerate(snippet["content"])
    )

    prompt = f"""
    You are a Python code reviewer. Analyze the following function:

    Filename: {snippet["filename"]}
    Language: {snippet["language"]}
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
            {"role": "system", "content": "You are an expert Python code reviewer."},
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
