import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API"))

# Specify the model name
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

# Specify the file path
file_path = "./static/data/wp-txt-data/about-me.txt"

# Read the file content
try:
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
        print("File Content:")
        print(file_content)
except FileNotFoundError:
    print(f"Error: File not found at path '{file_path}'. Please ensure the file exists.")
    exit()

# Interactive question-answer loop
while True:
    user_question = input("\nPlease ask your question (or type 'exit' to quit): ")
    
    if user_question.lower() in ['exit', 'q']:
        print("Exiting...")
        break

    try:
        # Generate content using the text data as context
        prompt = (
            "You are a helpful assistant. Only answer questions based on the provided text data. "
            "Do not answer any questions that are not based on the text data. "
            f"Text Data:\n{file_content}\n\n"
            f"User's Question: {user_question}"
        )

        response = model.generate_content(
            contents=prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
            stream=True,
            tools=None,
            tool_config=None,
            request_options=None
        )
        # print(response.text)
        for chunk in response:
                print(chunk.text, end='')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")
