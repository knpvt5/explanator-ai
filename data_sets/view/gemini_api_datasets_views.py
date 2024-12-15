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
from datasets import load_dataset
import pandas as pd

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
        
def gemini_raw_dataset_reader(request):
    return render(request, 'data_sets/gemini_api_datasets/gemini_raw_dataset_reader.html')

@csrf_exempt
@require_http_methods(["POST"])
def gemini_raw_dataset_reader_api(request):
    # Load the dataset
    dataset = load_dataset("knkrn5/wealthpsychology-raw-data", streaming=True)

    # Checking if the data has the tokenized format
    print(dataset)

    all_data = []

    # Print details of each split in the DatasetDict
    for split_name, split_data in dataset.items():
        split_rows = [row for row in split_data]
        split_df = pd.DataFrame(split_rows)
        all_data.append(split_df)
        
    print(split_df.head())
    print(all_data)
    print("\n" + "="*50 + "\n") #simple line separator
    

    try:
        body  = json.loads(request.body.decode("utf-8"))
        user_input = body.get("userInput")
        # Generate content using the text data as context
        
        prompt = (
            "You are a helpful assistant. Only answer questions based on the provided text data. "
            "Do not answer any questions that are not based on the text data. "
            f"Text Data:\n{all_data}\n\n"
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
