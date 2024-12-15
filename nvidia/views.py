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

def nvidia_api_chatbots(request):
    return render(request, 'nvidia/nvidia_api_chatbots.html')

def nvidia_url_reader(request):
    return render(request, 'nvidia/nvidia_url_reader.html')

def nvidia_txt_reader(request):
    return render(request, 'nvidia/nvidia_txt_reader.html')

def nvidia_csv_reader(request):
    return render(request, 'nvidia/nvidia_csv_reader.html')

def nvidia_json_reader(request):
    return render(request, 'nvidia/nvidia_json_reader.html')

def nvidia_pdf_reader(request):
    return render(request, 'nvidia/nvidia_pdf_reader.html')

# Generator function to stream API response chunks
def generate_stream_responses(response):
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            chunk_content = chunk.choices[0].delta.content
            yield f"data: {json.dumps({'chunk': chunk_content})}\n\n"

@csrf_exempt
@require_http_methods(["POST"])
def nvidia_api(request):
    """Handle user questions and interact with the NVIDIA API to provide responses."""
    try:
        # Parse the JSON payload
        data = json.loads(request.body.decode('utf-8'))
        user_input = data.get("question")
        
        if not user_input:
            return JsonResponse({"error": "No Question Provided."}, status=400)

        if not client:
            return JsonResponse({"error": "Service not available"}, status=503)

        # Create a streaming chat completion request
        response = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=512,
            temperature=0.7,
            top_p=0.95,
            stream=True
        )

        # Return a streaming response
        return StreamingHttpResponse(
            generate_stream_responses(response),
            content_type='text/event-stream'
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


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
def nvidia_txt_reader_api(request):
    # txt docs path
    txt_path = "./static/data/wp-txt-data/about-me.txt"

    # Open the file in read mode ('r')
    with open(txt_path, 'r', encoding='utf-8') as file:
        # Read the entire content of the file
        txt_content = file.read()
        print("Text read successfully.")

    if not txt_content:
        return JsonResponse({"error": "Failed to extract text from the URLs"}, status=500)


    try:
        # Parse user question from the POST request
        body = json.loads(request.body.decode("utf-8"))
        user_input = body.get("question")
        
        if not user_input:
            return JsonResponse({"error": "No question provided"}, status=400)
        
        print("Extracted URL Data Length:", len(txt_content))
        print("User Input:", user_input)

        # Create a completion request with the user question
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are an AI assistant. Only answer questions using the following text data. Do not use outside knowledge."},
                {"role": "assistant", "content": "I will answer questions only based on the provided text data."},
                {"role": "system", "content": f"Text Data:\n{txt_content}"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            # repetition_penalty=1.2,
            stream=True
        )

        print("API Response:", completion)
        return StreamingHttpResponse(generate_stream_responses(completion), content_type="text/event-stream")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def nvidia_csv_reader_api(request):
    csv_files = ['static/data/wp-csv-data/wp-pages.csv', 
                'static/data/wp-csv-data/wp-home.csv', 
                'static/data/wp-csv-data/blog-categories.csv', 
                'static/data/wp-csv-data/fin-calculators.csv', 
                'static/data/wp-csv-data/fin-quizzes.csv', 
                'static/data/wp-csv-data/contact-info.csv', 
                'static/data/wp-csv-data/about-us.csv', 
                'static/data/wp-csv-data/our-team.csv', 
                'static/data/wp-csv-data/our-plan.csv'
                ]

    # Function to extract text from CSV files
    def extract_csv_text(csv_files):
        all_data = []  # List to store combined data from all files
        for csv_data in csv_files:
            try:
                with open(csv_data, 'r', encoding='utf-8') as file:
                    csv_content = csv.DictReader(file)
                    for row in csv_content:
                        all_data.append(row)
            except Exception as e:
                print(f"Error reading CSV file {csv_data}: {e}")
        
        return all_data  # Return combined data from all files

    # Extract text from CSV files
    csv_text = extract_csv_text(csv_files)

    if not csv_text:
        print("Failed to extract text from the CSV. Please check the file paths and content.")
        exit()

    print("\nCSV Text Extracted Successfully!")

    # Convert combined data to text format for the model
    csv_text_str = "\n".join([str(row) for row in csv_text])  # Convert list of dictionaries to a string

    try: 
        body = json.loads(request.body.decode("utf-8"))
        user_input = body.get("question")

        # Create a completion request with the user question and extracted CSV text as context
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Only answer based on the provided CSV data. Do not answer any questions that are not based on the CSV data."},
                {"role": "assistant", "content": "I will only answer questions only based on the provided CSV data."},
                {"role": "system", "content": f"CSV Data:\n{csv_text_str}"},
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


    except Exception as e:
            print(f"Error occurred during completion request: {e}")


@csrf_exempt
@require_http_methods(["POST"])
def nvidia_json_reader_api(request):
    # List to store rows as dictionaries
    json_files = ['static/data/wp-json-data/wp-pages.json', 
                'static/data/wp-json-data/wp-home.json', 
                'static/data/wp-json-data/blog-categories.json', 
                'static/data/wp-json-data/fin-calculators.json', 
                'static/data/wp-json-data/fin-quizzes.json', 
                'static/data/wp-json-data/contact-info.json', 
                'static/data/wp-json-data/about-us.json', 
                'static/data/wp-json-data/our-team.json', 
                'static/data/wp-json-data/our-plan.json'
                ]


    # Function to extract text from json files
    def extract_json_text(json_files):
        all_data = []  # List to store combined data from all files
        for json_data in json_files:
            try:
                with open(json_data, 'r', encoding='utf-8') as jsonFile:
                    reader = json.load(jsonFile) # Parse the JSON content as python dictionary
                    for row in reader:
                        all_data.append(row)
            except Exception as e:
                print(f"Error reading JSON file {json_data}: {e}")
        
        return all_data  # Return combined data from all files

    # Extract text from json files
    json_text = extract_json_text(json_files)

    if not json_text:
        print("Failed to extract text from the JSON. Please check the file paths and content.")
        exit()

    print("\nJSON Text Extracted Successfully!")

    # Convert combined data to text format for the model
    json_text_str = "\n".join([str(row) for row in json_text])  # Convert list of dictionaries to a string

    

    try:
        body = json.loads(request.body.decode("utf-8"))
        user_input = body.get("question")
        
        # Create a completion request with the user question and extracted JSON text as context
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Only answer based on the provided JSON data. Do not answer any questions that are not based on the JSON data."},
                {"role": "assistant", "content": "I will only answer questions only based on the provided JSON data."},
                {"role": "system", "content": f"JSON Data:\n{json_text_str}"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            # repetition_penalty=1.2,
            stream=True
        )

        print("API Response:", completion)
        return StreamingHttpResponse(generate_stream_responses(completion), content_type="text/event-stream")

    except Exception as e:
        print(f"Error occurred during completion request: {e}")


@csrf_exempt
@require_http_methods(["POST"])
def nvidia_pdf_reader_api(request):
    # Function to extract text from a PDF file
    def extract_pdf_text(pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()  # Extract text from each page
        return text

    # Ask for PDF file path and extract the text
    pdf_path = "./static/data/wp-pdf-data/wp.pdf"
    pdf_text = extract_pdf_text(pdf_path)

    print("\nPDF Text Extracted Successfully!")

    
    try:
        body = json.loads(request.body.decode("utf-8"))
        user_input = body.get("question")
        
        # Create a completion request with the user question and extracted PDF text as context
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "system", "content": f"The content of the PDF is: {pdf_text[:20000]}..."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            # repetition_penalty=1.2,
            stream=True
        )
        
        return StreamingHttpResponse(generate_stream_responses(completion), content_type="text/even-steam")

    except Exception as e:
        print(f"Error occurred during completion request: {e}")

