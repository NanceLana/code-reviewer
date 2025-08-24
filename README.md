**LLM-Assisted Code Quality Assessment Tool**

This full-stack Python application analyzes code snippets using an LLM API (OpenAI) to provide automated code review comments and quality ratings. 

Please find the steps to run this app below:
1. Prerequisites
2. Installation 
3. Input File Format
4. Usage 
5. Troubleshooting

**Notes for assessment reviewer (Ms. Glaucia)** - The sample input json file is "snippets.json" and the sample output json file is "review_results".json. However, when you run the flask application, the input and output is seen as a pretty webpage. This webpage allows easy additions of the input snippets.

**PREREQUISITES**

- Python 3.7 or higher
- OpenAI API key

**INSTALLATION**

1. Clone or download this repository using command prompt

   git clone <https://github.com/NanceLana/code-reviewer>
   
   cd code-reviewer

2. Install required dependencies
   
   
   pip install -r requirements.txt
  

3. Set up your OpenAI API key
   
   Create a .env file in the 'code-reviewer' folder and add your OpenAI API key over there in the format:

   OPENAI_API_KEY= xxxx....

**USAGE**

1. Run the assessment tool in the command prompt inside the code-reviewer directory:
   
   python main.py

2. Input the required fields on the webpage: name of the file and the code snippet.

**TROUBLESHOOTING** 

1. API Key Not Set
   - Ensure the `OPENAI_API_KEY` environment variable is set correctly
   - Verify the API key is valid and has sufficient credits

2. Import Errors
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.7+)



