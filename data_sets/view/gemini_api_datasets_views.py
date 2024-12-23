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
from datasets import load_dataset
import pandas as pd
from ..controllers.gemini_api_ds.gemini_api_ds_ctrller import handle_gemini_raw_dataset_reader_request, handle_gemini_api_prompt_generator_ds_request


load_dotenv()

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
        
def gemini_api_prompt_generator_ds(request):
    return render(request, 'data_sets/gemini_api_datasets/gemini_api_prompt_generator_ds.html')

def gemini_raw_dataset_reader(request):
    return render(request, 'data_sets/gemini_api_datasets/gemini_raw_dataset_reader.html')

@csrf_exempt
@require_http_methods(["POST"])
def gemini_raw_dataset_reader_api(request):
    return handle_gemini_raw_dataset_reader_request(request, model, generate_stream_responses)


@csrf_exempt
@require_http_methods(["POST"])
def gemini_api_prompt_generator_ds_api(request):
    return handle_gemini_api_prompt_generator_ds_request(request, model, generate_stream_responses)