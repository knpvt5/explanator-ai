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
from datasets import load_dataset
import pandas as pd


load_dotenv(override=True)

# Initialize OpenAI client
client = None
try:
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API")
    )
except Exception as e:
    raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")


# Create your views here.
def nvidia_raw_dataset_reader(request):
    return render(request, 'data_sets/nvidia_api_datasets/nvidia_raw_dataset_reader.html')


# Generator function to stream API response chunks
def generate_stream_responses(response):
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            chunk_content = chunk.choices[0].delta.content
            yield f"data: {json.dumps({'chunk': chunk_content})}\n\n"


@csrf_exempt
@require_http_methods(["POST"])
def nvidia_raw_dataset_reader_api(request):
    # Load the dataset
    dataset = load_dataset("knkrn5/wealthpsychology-raw-data", streaming=True)

    # Checking if the data has the tokenized format
    # print(dataset)

    all_data = []

    # Print details of each split in the DatasetDict
    for split_name, split_data in dataset.items():
        split_rows = [row for row in split_data]
        split_df = pd.DataFrame(split_rows)
        all_data.append(split_df)

    # Print details of the DataFrame
    print(f"Split: {split_name}")
    print(split_df.head())
    print("\n" + "="*50 + "\n")

    try:
        body  = json.loads(request.body.decode("utf-8"))
        user_input = body.get('userInput')

        # Create a completion request with the user question
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": " your are an AI assistant."},
                {"role": "system", "content": f"dataset: {all_data}."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            # top_k = 50,
            top_p=0.7,
            max_tokens=1024,
            # repetition_penalty=1.2,
            stream=True
        )
        
        # return JsonResponse({"response": completion.choices[0].message.content})
        response =  StreamingHttpResponse(generate_stream_responses(completion), content_type="text/even-steam")
        response['Cache-Control'] = 'no-cache'
        return response

    except Exception as e:
        print(f"Error occurred during completion request: {e}")
        
        
        
