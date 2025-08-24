import json
from datetime import datetime
from reviewer import review_snippet

def format_code_with_line_numbers(code_content: str) -> str:
    """Format code with line numbers for better readability"""
    lines = code_content.split('\n')
    formatted_lines = []
    for i, line in enumerate(lines, 1):
        formatted_lines.append(f"{i:2d}: {line}")
    return '\n'.join(formatted_lines)

def convert_to_symbol_indentation(code_content: str) -> str:
    """Convert code with spaces to symbol-based indentation for LLM clarity"""
    lines = code_content.split('\n')
    symbol_lines = []
    
    for line in lines:
        if line.strip() == "":  # Empty line
            symbol_lines.append("")
            continue
            
        leading_spaces = len(line) - len(line.lstrip())
        indent_level = leading_spaces // 4  # Assuming 4 spaces per level
        
        # Create symbol representation
        if indent_level == 0:
            symbol = ""
        elif indent_level == 1:
            symbol = "*"
        elif indent_level == 2:
            symbol = "**"
        elif indent_level == 3:
            symbol = "***"
        else:
            symbol = "*" * indent_level
            
        # Add the symbol and the stripped line
        symbol_lines.append(f"{symbol}{line.strip()}")
    
    return '\n'.join(symbol_lines)

def main():
    # Load snippets
    with open("snippets.json", "r") as f:
        snippets_data = json.load(f)

    results = []

    for snippet in snippets_data.get("snippets", []):
        # Convert content array to string
        code_content = "\n".join(snippet["content"])
        
        # Convert to symbol-based indentation for LLM
        symbol_code = convert_to_symbol_indentation(code_content)
        
        review = review_snippet(snippet)
        results.append({
            "id": snippet["id"],
            "filename": snippet["filename"],
            "language": snippet.get("language", ""),
            "code": code_content,
            "code_formatted": format_code_with_line_numbers(code_content),
            "code_symbols": symbol_code,
            "review": review
        })

    # Wrap results with timestamp
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "results": results
    }

    # Ensure output folder exists
    import os
    os.makedirs("output", exist_ok=True)

    # Save results to JSON
    with open("output/review_results.json", "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"-> Review results saved to output/review_results.json")
    print(f"-> Processed {len(results)} code snippets")

if __name__ == "__main__":
    main()
