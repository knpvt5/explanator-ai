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

text_file = "static/data/wp-txt-data/about-me.txt"

urls = ['https://wealthpsychology.in/index.html',
    'https://wealthpsychology.in/blog/',
    ]

# List to store rows as dictionaries
csv_files = ['static/data/wp-csv-data/wp-pages.csv',
            'static/data/wp-csv-data/wp-home.csv', 
            ]

json_files = ['static/data/wp-json-data/wp-pages.json',
                'static/data/wp-json-data/wp-home.json',
                ]

pdf_files = ["./static/data/wp-pdf-data/wp.pdf",]


# Initialize the OpenAI client with NVIDIA's base URL and API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

# Function to extract text from CSV files
def extract_all_files_data():
    all_data = []  # List to store combined data from all files
    
    # Parsing txt file
    with open(text_file, 'r', encoding='utf-8') as textFile:    
        text_content = textFile.read()
        all_data.append({
            'text_content': text_content
        })
    print(f"Total text data from {text_file}: {text_content}")
    print("="*100 + "\n")
    
    
    # Parsing CSV files
    for csv_file in csv_files:
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

    # Parsing JSON files
    for json_file in json_files:
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
            
    # Parsing URLs   
    for url in urls:
        urlsData = []
        try:
            response  = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator="\n")
            cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
            # formatted_text = "\n\n".join(cleaned_text)
            urlsData.append({
                'url': url,
                'text_content': cleaned_text
            })
            all_data.append(urlsData)
            print(f"Total URLs data from {url}: {urlsData}")
            print("="*100 + "\n")
        except Exception as e:
            print(f"Error fetching {url}: {e}")

            
    # parsing PDF files
    for pdf_data in pdf_files:
        pdfData = []
        try:
            with open(pdf_data, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()  # Extract text from each page
                pdfData.append({
                    'pdf_data': text,
                })
            print(f"Total PDF data from {pdf_data}: {pdfData}")
            print("="*100 + "\n")
            all_data.append(pdfData)
        except Exception as e:
            print(f"Error reading PDF file {pdf_data}: {e}")
            
    
    return all_data 

# Extract text from CSV files
all_files_data = extract_all_files_data()
print("\nAll Files Extracted Successfully!")
# Convert combined data to text/string format for the model
all_files_data_str = "\n".join([str(row) for row in all_files_data])
print(f"Analyzing text with length: {len(all_files_data_str)}")
print("all data", all_files_data_str)


if not all_files_data_str:
    print("Failed to extract text from the CSV. Please check the file paths and content.")
    exit()


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
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Only answer based on the provided data. Do not answer any questions that are not based on the data."},
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

