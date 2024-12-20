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
