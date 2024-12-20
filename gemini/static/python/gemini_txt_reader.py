import os
import google.generativeai as genai
from dotenv import load_dotenv
import csv
import json
import PyPDF2

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API"))

# Specify the model name
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

# Specify the file path
files = ["static/eg_data/eg-txt-data/eg.txt",
    "static/eg_data/eg-csv-data/eg1.csv",
    "static/eg_data/eg-json-data/eg1.json",
    "static/eg_data/eg-pdf-data/eg.pdf",
    ]

all_Data = []

for filename in files:
    if filename.endswith(".txt"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                file_content = file.read()
                all_Data.append(file_content)
                print(f"txt file data: {file_content}")
        except FileNotFoundError:
            print(f"Error: File not found at path '{filename}'. Please ensure the file exists.")
            
    elif filename.endswith(".csv"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                CSVreader = csv.DictReader(file)
                for CSVrow in CSVreader:
                    all_Data.append(CSVrow)
                    print(f"csv file data: {CSVrow}")
        except FileNotFoundError:
            print(f"Error: File not found at path '{filename}'. Please ensure the file exists.")
            
    elif filename.endswith(".json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                JSONreader = json.load(file)
                for JSONrow in JSONreader:
                    all_Data.append(JSONrow)
                    print(f"json file data: {JSONrow}")
        except FileNotFoundError:
            print(f"Error: File not found at path '{filename}'. Please ensure the file exists.")
            
    elif filename.endswith(".pdf"):
        try:
            with open(filename, "rb") as file:
                PDFreader = PyPDF2.PdfReader(file)
                for page in PDFreader.pages:
                    text = page.extract_text()
                    all_Data.append(text)
                    print(f"pdf file data: {text}")
        except FileNotFoundError:
            print(f"Error: File not found at path '{filename}'. Please ensure the file exists.")
            
            
if all_Data:
    all_Data_str = str(all_Data)
    file_content = "\n".join(all_Data_str)    
    
    # Interactive question-answer loop
    while True:
        user_input = input("\nPlease ask your question (or type 'exit' to quit): ")
        
        if user_input.lower() in ['exit', 'q']:
            print("Exiting...")
            break

        try:
            # Generate content using the text data as context
            prompt = (
                "You are a helpful assistant. Only answer questions based on the provided text data. "
                "Do not answer any questions that are not based on the text data. "
                f"Text Data:\n{file_content}\n\n"
                f"User's Question: {user_input}"
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
