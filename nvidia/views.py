from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from openai import OpenAI
from dotenv import load_dotenv
import json
import csv
import PyPDF2
from bs4 import BeautifulSoup
import requests
import os
import asyncio
from .controllers.nvidia_api_cb_ctrller import handle_nvidia_api_cb_request

# Load environment variables
load_dotenv(override=True)

# Get API key and verify it exists
NVIDIA_API_KEY = os.getenv("NVIDIA_API")
if not NVIDIA_API_KEY:
    raise RuntimeError("NVIDIA API key not found!")

# Initialize OpenAI client
client = None
try:
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY
    )
except Exception as e:
    raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")

def nvidia(request):
    return render(request, 'nvidia/nvidia.html')

def nvidia_docs_analyzer(request):
    return render(request, 'nvidia/nvidia_docs_analyzer.html')

def nvidia_api_chatbots(request):
    return render(request, 'nvidia/nvidia_api_chatbots.html')

def nvidia_url_reader(request):
    return render(request, 'nvidia/nvidia_url_reader.html')


# Generator function to stream API response chunks
def generate_stream_responses(response):
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            chunk_content = chunk.choices[0].delta.content
            yield f"data: {json.dumps({'chunk': chunk_content})}\n\n"

@csrf_exempt
@require_http_methods(["POST"])
def nvidia_api(request):
    return handle_nvidia_api_cb_request(request, client, generate_stream_responses)

@csrf_exempt
@require_http_methods(["POST"])
def nvidia_url_reader_api(request):
    urls = [
        "https://wealthpsychology.in/index.html",
        "https://wealthpsychology.in/blog/",
        "https://wealthpsychology.in/financial-calculators/",
        "https://wealthpsychology.in/finance-quizzes/",
        "https://wealthpsychology.in/contact-us/",
        "https://wealthpsychology.in/about-us/",
        "https://wealthpsychology.in/our-team/",
        "https://wealthpsychology.in/our-plan/"
    ]

    def clean_text(text):
        cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(cleaned_lines)

    all_data = []

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            content = "\n".join(
            element.get_text(strip=True) for element in soup.find_all(["p", "h1", "h2", "a", "li"])
            )
            cleaned_content = clean_text(content)
            all_data.append(cleaned_content)
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            all_data.append(f"Error fetching {url}: {e}")

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    try:
        user_input = data.get("question", "").strip()

        if not user_input:
            return JsonResponse({"error": "No input provided"}, status=400)

        print("Extracted URL Data Length:", len(all_data))
        print("User Input:", user_input)

        text_data = "\n\n".join(all_data)
        
        # Replace this with your model's API call
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are an AI assistant analyzing web content. Provide concise and helpful responses based on the provided URL data."},
                {"role": "user", "content": f"URL Data:\n{text_data}\n\nQuestion: {user_input}"}
            ],
            temperature=0.5,
            max_tokens=512,
            stream=True,
        )

        print("API Response:", completion)

        return StreamingHttpResponse(generate_stream_responses(completion), content_type="text/event-stream")

    except Exception as e:
        print(f"Unexpected error: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def nvidia_docs_analyzer_api(request):

    files = ["static/eg_data/eg-txt-data/eg.txt",
                "static/eg_data/eg-csv-data/eg1.csv",
                "static/eg_data/eg-json-data/eg1.json",
                "static/eg_data/eg-pdf-data/eg.pdf",
                ]
    
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_input = data.get("userInput")
        model_name = data.get("modelName")
        
        if not user_input:
            return JsonResponse({"error": "No Question Provided."}, status=400)

        if not model_name:
            model_name = "nvidia/llama-3.1-nemotron-70b-instruct"
            print(model_name)

        if not client:
            return JsonResponse({"error": "Service not available"}, status=503)

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
            print("Failed to extract text from the CSV. Please check the file paths and content.")
            exit()

            
        # Create a completion request with the user question and extracted CSV text as context
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

        # Stream the response chunks and print them
        return StreamingHttpResponse(generate_stream_responses(completion), content_type="text/event-stream")

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



