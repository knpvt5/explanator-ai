# views.py in your 'nvidia' app
import os
from django.shortcuts import render, redirect
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import google.generativeai as genai
import csv
import json
from bs4 import BeautifulSoup 
import requests
from .controllers.gemini_api_cb_ctrller import handle_gemini_api_cb_request
from .controllers.gemini_docs_analyzer_ctrller import handle_gemini_docs_analyzer_request

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API"))
model = genai.GenerativeModel("gemini-1.5-flash")


""" def gemini(request):
    return render(request, 'gemini/gemini.html') """

def gemini_api_cb(request):
    if request.headers.get('X-Requested-With') == 'homeNavFetch':
        return render(request, 'gemini/gemini_api_cb.html')
    else:
        return redirect('/?ai=gemini&aiType=gemini-api-cb')

def gemini_docs_analyzer(request):
    if request.headers.get('X-Requested-With') == 'homeNavFetch':
        return render(request, 'gemini/gemini_docs_analyzer.html')
    else:
        return redirect('/?ai=gemini&aiType=gemini-docs-analyzer')


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

@csrf_exempt
@require_http_methods(["POST"])
def gemini_docs_analyzer_api(request):
    #for debugging
    print("Request received")
    print("Request method:", request.method)
    print("Content type:", request.content_type)
    print("Files:", request.FILES)
    
    return handle_gemini_docs_analyzer_request(request, model, generate_stream_responses)