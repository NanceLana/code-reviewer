**LLM-Assisted Code Quality Assessment Tool**

This full-stack Python application analyzes code snippets using an LLM API (OpenAI) to provide automated code review comments and quality ratings. 

Please find the steps to run this app below:
1. Prerequisites
2. Installation 
3. Input File Format
4. Usage 
5. Troubleshooting

**PREREQUISITES**

- Python 3.7 or higher
- OpenAI API key

**INSTALLATION**

1. Clone or download this repository using command prompt

   git clone <repository-url>
   cd Deliverable

2. Install required dependencies
   
   
   pip install -r requirements.txt
  

3. Set up your OpenAI API key
   
   Create a .env file and add your OpenAI API key over there in the format:
   OPENAI_API_KEY= 


**INPUT FILE FORMAT**

The tool accepts JSON files with the following structure:

```json
{
  "snippets": [
    {
      "id": 1,
      "filename": "example.py",
      "language": "python",
      "content": [
        "def your_function():",
        "    # Your code here",
        "    pass"
      ]
    }
  ]
}
```

**Note**: The `content` field should be an array of strings, where each string represents a line of code.



**USAGE**



1. Run the assessment tool:
   
   python main.py

2. Input the required fields like name of the file, language and the code snippet.


**TROUBLESHOOTING** 

1. API Key Not Set
   - Ensure the `OPENAI_API_KEY` environment variable is set correctly
   - Verify the API key is valid and has sufficient credits

2. Import Errors
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.7+)

3. API Rate Limits
   - The tool includes error handling for API failures
   - Check your OpenAI account for rate limits and usage

4. Invalid Input Format
   - Ensure your JSON file is properly formatted
   - Check that each snippet has a `content` field

