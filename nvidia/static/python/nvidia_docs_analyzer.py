import os
from dotenv import load_dotenv
from openai import OpenAI
from bs4 import BeautifulSoup
import requests
import csv
import json
import PyPDF2

# Load environment variables
load_dotenv()

files = ["static/eg_data/eg-txt-data/eg.txt",
            "static/eg_data/eg-csv-data/eg1.csv",
            "static/eg_data/eg-json-data/eg1.json",
            "static/eg_data/eg-pdf-data/eg.pdf",
            ]

#model options
models = {
    "1": "nvidia/llama-3.1-nemotron-70b-instruct",
    "2": "meta/llama-3.3-70b-instruct",
    "3": "nv-mistralai/mistral-nemo-12b-instruct",
    "4": "microsoft/phi-3-mini-128k-instruct",
}

# Prompt user to select a model
print("Select a model:")
for key, value in models.items():
    print(f"{key}. {value}")

# Validate user input in a loop
while True:
    model_choice = input("\nEnter the number corresponding to the model: ")
    if model_choice in models:
        model_name = models[model_choice]
        break
    else:
        print("Invalid choice. Please enter a valid number.")

print("Using model:", model_name)

# Initialize the OpenAI client with NVIDIA's base URL and API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

# Function to extract text from CSV files
def extract_all_files_data():
    all_data = []  
    
    # Parsing text files
    for text_file in files:
        if text_file.endswith(".txt"):
            if not text_file or not os.path.exists(text_file): 
                print(f"Text file {text_file} does not exist or is incorrect path, skipping...")
                print("="*100 + "\n")
                continue  

            try:
                with open(text_file, 'r', encoding='utf-8') as textFile:
                    text_content = textFile.read()
                    all_data.append({
                        'text_content': text_content
                    })
                print(f"Total text data from {text_file}: {text_content}")
                print("="*100 + "\n")
            except Exception as e:
                print(f"Error reading text file {text_file}: {e}")
        else:
            continue

    
    
    # Parsing CSV files
    for csv_file in files:
        if csv_file.endswith(".csv"):
            if not csv_file or not os.path.exists(csv_file): 
                print(f"CSV file {csv_file} does not exist or is incorrect path, skipping...")
                print("="*100 + "\n")
                continue
            
            csvData = []
            try:
                with open(csv_file, 'r', encoding='utf-8') as file:
                    CSVreader = csv.DictReader(file)
                    for CSVrow in CSVreader:
                        csvData.append(CSVrow)
                print(f"Total CSV data from {csv_file}: {csvData}")
                print("="*100 + "\n")
                all_data.append(csvData)  # Append the data to the main list
            except Exception as e:
                print(f"Error reading CSV file {csv_file}: {e}")
        else:
            continue

    # Parsing JSON files
    for json_file in files:
        if json_file.endswith(".json"):
            if not json_file or not os.path.exists(json_file): 
                print(f"JSON file {json_file} does not exist or is incorrect path, skipping...")
                print("="*100 + "\n")
                continue  
            
            jsonData = []
            try:
                with open(json_file, 'r', encoding='utf-8') as jsonFile:
                    JSONreader = json.load(jsonFile)
                    for JSONrow in JSONreader:
                        jsonData.append(JSONrow)
                print(f"Total JSON data from {json_file}: {jsonData}")
                print("="*100 + "\n")
                all_data.append(jsonData)
            except Exception as e:
                print(f"Error reading JSON file {json_file}: {e}")
        else:
            continue

            
    # parsing PDF files
    for pdf_file in files:
        if pdf_file.endswith(".pdf"):
            if not pdf_file or not os.path.exists(pdf_file): 
                print(f"PDF file {pdf_file} does not exist or is incorrect path, skipping...")
                print("="*100 + "\n")
                continue  
            
            pdfData = []
            try:
                with open(pdf_file, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()  # Extract text from each page
                    pdfData.append({
                        'pdf_data': text,
                    })
                print(f"Total PDF data from {pdf_file}: {pdfData}")
                print("="*100 + "\n")
                all_data.append(pdfData)
            except Exception as e:
                print(f"Error reading PDF file {pdf_file}: {e}")
        else:
            continue
                
    
    return all_data 

# Extract text from CSV files
all_files_data = extract_all_files_data()
print("\nAll Files Extracted Successfully!")
# Convert combined data to text/string format for the model
all_files_data_str = "\n".join([str(row) for row in all_files_data])
print(f"Analyzing text with length: {len(all_files_data_str)}")
print("all data", all_files_data_str)

if not all_files_data_str:
    print("No data provided, continuing without any file...")


while True:
    # Take user input for the question
    user_question = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    # Exit the loop if the user types 'exit' or 'q'
    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    try:
        # Create a completion request with the user question and extracted CSV text as context
        completion = client.chat.completions.create(
            model= model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Only answer based on the provided data. Do not answer any questions that are not based on the data provided."},
                {"role": "assistant", "content": "I will only answer questions only based on the provided data."},
                {"role": "system", "content": f"Data:\n{all_files_data_str}"},
                {"role": "user", "content": user_question}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            # repetition_penalty=1.2,
            stream=True
        )

        # Stream the response chunks and print them
        print("\nAI Response:")
        for chunk in completion:
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="")
        print()  # For newline after the streamed response

    except Exception as e:
        print(f"Error occurred during completion request: {e}")

