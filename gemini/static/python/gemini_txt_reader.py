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

# Specify the file paths
files = [
    "static/eg_data/eg-txt-data/eg.txt",
    "static/eg_data/eg-csv-data/eg1.csv",
    "static/eg_data/eg-json-data/eg1.json",
    "static/eg_data/eg-pdf-data/eg.pdf",
]

all_Data = []

for filename in files:
    if filename.endswith(".txt"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                text_content = file.read()
                all_Data.append(text_content)
                print(f"txt file data: {text_content}\n")
        except FileNotFoundError:
            print(f"Error: File not found at path '{filename}'. Please ensure the file exists.\n")
            
    elif filename.endswith(".csv"):
        csvData = []
        try:
            with open(filename, "r", encoding="utf-8") as csvFile:
                CSVreader = csv.DictReader(csvFile)
                for CSVrow in CSVreader:
                    csvData.append(CSVrow)
                print(f"CSV file data: {csvData}\n")
                all_Data.append(csvData)
        except FileNotFoundError:
            print(f"Error: File not found at path '{filename}'. Please ensure the file exists.\n")
            
    elif filename.endswith(".json"):
        jsonData = []
        try:
            with open(filename, "r", encoding="utf-8") as jsonFile:
                JSONreader = json.load(jsonFile)
                for JSONrow in JSONreader:
                    jsonData.append(JSONrow)
                print(f"json file data: {jsonData}\n")
                all_Data.append(jsonData)
        except FileNotFoundError:
            print(f"Error: File not found at path '{filename}'. Please ensure the file exists.\n")
            
    elif filename.endswith(".pdf"):
        pdfData = []
        try:    
            with open(filename, "rb") as pdfFile:
                PDFreader = PyPDF2.PdfReader(pdfFile)
                for page in PDFreader.pages:
                    text = page.extract_text()
                    pdfData.append(text)
                print(f"pdf file data: {pdfData}\n")
                all_Data.append(pdfData)
        except FileNotFoundError:
            print(f"Error: File not found at path '{filename}'. Please ensure the file exists.\n")
    else:
        print(f"Unsupported file format: {filename}")

# Convert all data to string format
all_Data_str = str(all_Data) if all_Data else ""
print("all data string:", all_Data_str)

if not all_Data:
    print("No data extracted. Exiting...")
else:
    # Main question-answering loop
    while True:
        user_input = input("\nPlease ask your question (or type 'exit' to quit): ")
        
        if user_input.lower() in ['exit', 'q']:
            print("Exiting...")
            break

        try:
            # Generate content using the text data as context
            prompt = (
                # "You are a helpful assistant. Only answer questions based on the provided text data. "
                # "Do not answer any questions that are not based on the text data. "
                f"Text Data:\n{all_Data_str}\n\n"
                f"User's Input: {user_input}"
            )

            response = model.generate_content(
                contents=prompt,
                generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
                stream=True,
                tools=None,
                tool_config=None,
                request_options=None
            )
            
            for chunk in response:
                print(chunk.text, end='')
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again or check your API key and internet connection.")