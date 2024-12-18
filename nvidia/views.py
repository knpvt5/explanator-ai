from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from openai import OpenAI
from dotenv import load_dotenv
import json
from bs4 import BeautifulSoup
import requests
import os
import asyncio
from .controllers.nvidia_api_cb_ctrller import handle_nvidia_api_cb_request
from .controllers.nvidia_docs_analyzer_ctrller import handle_nvidia_docs_analyzer_request

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
    return handle_nvidia_docs_analyzer_request(request, client, generate_stream_responses)
    