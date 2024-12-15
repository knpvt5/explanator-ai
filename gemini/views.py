# views.py in your 'nvidia' app
import os
from django.shortcuts import render
import json
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import csv
import json
from bs4 import BeautifulSoup 
import PyPDF2
import asyncio

load_dotenv()

def gemini(request):
    return render(request, 'gemini/gemini.html')

def gemini_api_chatbots(request):
    return render(request, 'gemini/gemini_api_chatbots.html')

def gemini_url_reader(request):
    return render(request, 'gemini/gemini_url_reader.html')

def gemini_txt_reader(request):
    return render(request, 'gemini/gemini_txt_reader.html')

def gemini_csv_reader(request):
    return render(request, 'gemini/gemini_csv_reader.html')

def gemini_json_reader(request):
    return render(request, 'gemini/gemini_json_reader.html')

def gemini_pdf_reader(request):
    return render(request, 'gemini/gemini_pdf_reader.html')


# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API"))
model = genai.GenerativeModel("gemini-1.5-flash")


# Function to stream the chunks back to the client
def generate_stream_responses(response):
    try:
        for chunk in response:
            # Yield the chunk as a part of the streaming response
            yield f"data: {json.dumps({'chunk': chunk.text})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
        

# View to handle Gemini chatbot requests
@csrf_exempt
def gemini_api(request):
    if request.method == "POST":
        try:
            # Parse and validate the request body
            body = json.loads(request.body)
            user_input = body.get("question", "")
            if not user_input:
                return JsonResponse({"error": "No question provided"}, status=400)

            # Define safety settings
            safety_settings = [
                {"category": "HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            ]

            # Generate response using the model
            try:
                response = model.generate_content(
                    user_input,
                    generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
                    safety_settings=safety_settings,
                    stream=True,
                )

                # Stream the response back to the client
                return StreamingHttpResponse(
                    generate_stream_responses(response),
                    content_type    ="text/event-stream",
                )

            except Exception as model_error:
                return JsonResponse({"error": f"Model Error: {str(model_error)}"}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
        except Exception as general_error:
            return JsonResponse({"error": f"Unexpected Error: {str(general_error)}"}, status=500)

    # Return error for non-POST requests
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@require_http_methods(["POST"])
def gemini_url_reader_api(request):
    urls = [
        "https://wealthpsychology.in/index.html",
        "https://wealthpsychology.in/blog/",
        "https://wealthpsychology.in/financial-calculators/",
        "https://wealthpsychology.in/finance-quizzes/",
        "https://wealthpsychology.in/contact-us/",
        "https://wealthpsychology.in/about-us/",
        "https://wealthpsychology.in/our-team/",
        "https://wealthpsychology.in/our-plans/"
    ]

    def extract_all_text(urls):
        all_text = []
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                # If the request was successful
                if response.ok:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text(separator="\n")
                    cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
                    all_text.append(cleaned_text)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {e}")

        return "\n\n".join(all_text)

    # Extract website data
    site_data = extract_all_text(urls)

    # Validate extracted data
    if not site_data:
        return JsonResponse({"error": "Failed to extract text from the URLs"}, status=500)

    try:
        # Parse user question from the POST request
        body = json.loads(request.body.decode("utf-8"))
        user_input = body.get("question")

        if not user_input:
            return JsonResponse({"error": "No question provided"}, status=400)

        print("Extracted URL Data Length:", len(site_data))
        print("User Input:", user_input)

        # Build the prompt for Gemini AI
        prompt = (
            "You are a helpful assistant. Use the following text data from the website to answer the user's question. "
            "Only provide answers based on the text data provided. If the answer is not in the text, respond with "
            "'The answer is not available in the provided data.'\n\n"
            f"Website Data:\n{site_data}\n\n"
            f"User's Question: {user_input}"
        )

        # Generate response using Gemini AI
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
            stream=True,  # Ensures the response is streamed in chunks
        )


        return StreamingHttpResponse(generate_stream_responses(response), content_type="text/event-stream")

    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def gemini_txt_reader_api(request):

    # Specify the file path
    file_path = "./static/data/wp-txt-data/about-me.txt"
    
    if not file_path:
        print("Failed to extract text. Please check the file paths and content.")
        exit()

    # Read the file content
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
            print("File Content:")
            print(file_content)
    except FileNotFoundError:
        print(f"Error: File not found at path '{file_path}'. Please ensure the file exists.")
        exit()

    try:
        # Parse user question from the POST request
        body = json.loads(request.body.decode("utf-8"))
        user_input = body.get("question")
        
        if not user_input:
            return JsonResponse({"error": "No question provided"}, status=400)
        
        print("Extracted URL Data Length:", len(file_content))
        print("User Input:", user_input)


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
        return StreamingHttpResponse(generate_stream_responses(response), content_type="text/event-stream")

                    
    except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again or check your API key and internet connection.")


@csrf_exempt
@require_http_methods(["POST"])
def gemini_csv_reader_api(request):
    # Specify the file path
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


    csv_text_str = "\n".join([str(row) for row in csv_text])  # Convert list of dictionaries to a string
    print(csv_text_str)


    try:
        body = json.loads(request.body.decode("utf-8"))
        user_input = body.get("question")
        
        print("Extracted URL Data Length:", len(csv_text))
        print("User Input:", user_input)
        
        if not user_input:
            return JsonResponse({"error": "No question provided"}, status=400)
        # Generate content using the text data as context
        prompt = (
            "You are a helpful assistant. Only answer questions based on the provided data. "
            "Do not answer any questions that are not based on the  data. "
            f"Text Data:\n{csv_text}\n\n"
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
        
        return StreamingHttpResponse(generate_stream_responses(response), content_type="text/event-stream")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")


@csrf_exempt
@require_http_methods(["POST"])
def gemini_json_reader_api(request):
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

    # Specify the model name
    model_name = "gemini-1.5-flash"
    model = genai.GenerativeModel(model_name)

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
    json_text_str = "\n".join([str(row) for row in json_text])


    try:
        body = json.loads(request.body)
        user_input  = body.get("question")
        
        
        # Generate content using the text data as context
        prompt = (
            "You are a helpful assistant. Only answer questions based on the provided text data. "
            "Do not answer any questions that are not based on the text data. "
            f"Text Data:\n{json_text_str}\n\n"
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
        return StreamingHttpResponse(generate_stream_responses(response), content_type="text/event-stream")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")


@csrf_exempt
@require_http_methods(["POST"])
def gemini_pdf_reader_api(request):
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
        
        print("Extracted URL Data Length:", len(pdf_text))
        # Generate content using the text data as context
        prompt = (
            "You are a helpful assistant. Only answer questions based on the provided data. "
            "Do not answer any questions that are not based on the data. "
            f"Text Data:\n{pdf_text}\n\n"
            f"User's Question: {user_input}"
        )
        

        response = model.generate_content(
            contents=prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
            stream=True,
        )
        
        return StreamingHttpResponse(generate_stream_responses(response), content_type="text/event-stream")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")


