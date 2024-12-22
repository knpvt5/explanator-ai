import os
import google.generativeai as genai
from dotenv import load_dotenv
import csv
import json
import PyPDF2
import logging

# Config logging 
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
)

# Initialize logging
logger = logging.getLogger(__name__)

load_dotenv()

# Gemini API
genai.configure(api_key=os.getenv("GEMINI_API"))

#model name
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

files = []

all_Data = []

for filename in files:
    try:
        if filename.endswith(".txt"):
            with open(filename, "r", encoding="utf-8") as file:
                text_content = file.read()
                all_Data.append(text_content)
                print(f"txt file data: {text_content}\n")
                
        elif filename.endswith(".csv"):
            csvData = []
            with open(filename, "r", encoding="utf-8") as csvFile:
                CSVreader = csv.DictReader(csvFile)
                for CSVrow in CSVreader:
                    csvData.append(CSVrow)
                print(f"CSV file data: {csvData}\n")
                all_Data.append(csvData)

        elif filename.endswith(".json"):
            jsonData = []
            with open(filename, "r", encoding="utf-8") as jsonFile:
                JSONreader = json.load(jsonFile)
                for JSONrow in JSONreader:
                    jsonData.append(JSONrow)
                print(f"json file data: {jsonData}\n")
                all_Data.append(jsonData)
            
        elif filename.endswith(".pdf"):
            pdfData = []
            with open(filename, "rb") as pdfFile:
                PDFreader = PyPDF2.PdfReader(pdfFile)
                for page in PDFreader.pages:
                    text = page.extract_text()
                    pdfData.append(text)
                print(f"pdf file data: {pdfData}\n")
                all_Data.append(pdfData)
        else:
            logging.info(f"Unsupported file format: {filename}")
    except FileNotFoundError:
            logging.info(f"Error: File not found at path '{filename}'. Please ensure the file exists.\n")


# Converting all data to str
all_Data_str = str(all_Data) if all_Data else ""
logging.info("all data string:", all_Data_str)

if not all_Data:
    print("No data extracted. Exiting...")
else:

    while True:
        user_input = input("\nPlease ask your question (or type 'exit' to quit): ")
        
        if user_input.lower() in ['exit', 'q']:
            print("Exiting...")
            break

        try:
            prompt = (
                # "You are a helpful assistant. Only answer questions based on the provided data. "
                # "Do not answer any questions that are not based on the data. "
                f"Data:\n{all_Data_str}\n\n"
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