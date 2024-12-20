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
from .controllers.gemini_api_cb_ctrller import handle_gemini_api_cb_request

load_dotenv()

def gemini(request):
    return render(request, 'gemini/gemini.html')

def gemini_api_cb(request):
    return render(request, 'gemini/gemini_api_cb.html')

def gemini_docs_analyzer(request):
    return render(request, 'gemini/gemini_docs_analyzer.html')


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
    return handle_gemini_api_cb_request(request, model, generate_stream_responses)