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

def nvidia_api_cb(request):
    return render(request, 'nvidia/nvidia_api_cb.html')

def nvidia_docs_analyzer(request):
    return render(request, 'nvidia/nvidia_docs_analyzer.html')


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
def nvidia_docs_analyzer_api(request):
    return handle_nvidia_docs_analyzer_request(request, client, generate_stream_responses)
    