import os
from dotenv import load_dotenv
from openai import OpenAI
from bs4 import BeautifulSoup
import requests
import csv
import json
import PyPDF2

load_dotenv()


files = []


#model options
models = {
    "1": "nvidia/llama-3.1-nemotron-70b-instruct",
    "2": "meta/llama-3.3-70b-instruct",
    "3": "nv-mistralai/mistral-nemo-12b-instruct",
    "4": "microsoft/phi-3-mini-128k-instruct",
}

# select a model
print("Select a model:")
for key, value in models.items():
    print(f"{key}. {value}")

while True:
    model_choice = input("\nEnter the number corresponding to the model: ")
    if model_choice in models:
        model_name = models[model_choice]
        break
    else:
        print("Invalid choice. Please enter a valid number.")

print("Using model:", model_name)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

# Extract data function
def extract_all_files_data():
    all_data = []  
    
    # Parsing data from files
    for file in files:
        try:
            if file.endswith(".txt"):
                text_file = file
                with open(text_file, 'r', encoding='utf-8') as textFile:
                    text_content = textFile.read()
                    all_data.append({
                        'text_content': text_content
                    })
                print(f"Total text data from {text_file}: {text_content}\n")
                
            elif file.endswith(".csv"):
                csv_file = file
                csvData = []
                with open(csv_file, 'r', encoding='utf-8') as file:
                    CSVreader = csv.DictReader(file)
                    for CSVrow in CSVreader:
                        csvData.append(CSVrow)
                print(f"Total CSV data from {csv_file}: {csvData}\n")
                all_data.append(csvData) 
                    
            elif file.endswith(".json"):
                json_file = file
                jsonData = []
                with open(json_file, 'r', encoding='utf-8') as jsonFile:
                    JSONreader = json.load(jsonFile)
                    for JSONrow in JSONreader:
                        jsonData.append(JSONrow)
                print(f"Total JSON data from {json_file}: {jsonData}\n")
                all_data.append(jsonData)
                    
            elif file.endswith(".pdf"):
                pdf_file = file
                pdfData = []
                with open(pdf_file, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()  # Extract text from each page
                    pdfData.append({
                        'pdf_data': text,
                    })
                print(f"Total PDF data from {pdf_file}: {pdfData}\n")
                all_data.append(pdfData)

        except FileNotFoundError:
            print(f"Error: File not found at path '{file}'. Please ensure the file exists.\n")

    return all_data 

# Extract data
all_files_data_str = ""
all_files_data = extract_all_files_data()
if all_files_data:
    all_files_data_str = "\n".join([str(row) for row in all_files_data])
    print("\nExtracted", len(all_files_data_str), "Character Successfully!")
    print("all data", all_files_data_str)
    if not all_files_data_str:
        print("No data provided, continuing without any file...")
else:
    print("No data extracted. continuing without any Data provided...")


while True:
    # user input 
    user_input = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    if user_input.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    try:
        # completion 
        completion = client.chat.completions.create(
            model= model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Only answer based on the provided data. Do not answer any questions that are not based on the data provided."},
                {"role": "assistant", "content": "I will only answer questions only based on the provided data."},
                {"role": "system", "content": f"Data:\n{all_files_data_str}"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            # repetition_penalty=1.2,
            stream=True
        )

        # Streaming response 
        print("\nAI Response:")
        for chunk in completion:
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="")

    except Exception as e:
        print(f"Error occurred during completion request: {e}")

