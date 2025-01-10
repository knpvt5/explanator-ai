from django.shortcuts import render, redirect
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
from ..controllers.nvidia_api_ds.nvidia_api_ds_ctrller import handle_nvidia_raw_dataset_reader_request, handle_nvidia_api_prompt_generator_ds_request


load_dotenv(override=True)

#OpenAI client
client = None
try:
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API")
    )
except Exception as e:
    raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")


#views here.
def nvidia_api_prompt_generator_ds(request):
    if request.headers.get('X-Requested-With') == 'homeNavFetch':
        return render(request, 'data_sets/nvidia_api_datasets/nvidia_api_prompt_generator_ds.html')
    else:
        return redirect('/?ai=nvidia&aiType=nvidia-api-prompt-generator-ds')
    

def nvidia_raw_dataset_reader(request):
    if request.headers.get('X-Requested-With') == 'homeNavFetch':
        return render(request, 'data_sets/nvidia_api_datasets/nvidia_raw_dataset_reader.html')
    else:
        return redirect('/?ai=nvidia&aiType=nvidia-raw-dataset-reader')


# Generator function to stream API response chunks
def generate_stream_responses(response):
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            chunk_content = chunk.choices[0].delta.content
            yield f"data: {json.dumps({'chunk': chunk_content})}\n\n"


@csrf_exempt
@require_http_methods(["POST"])
def nvidia_raw_dataset_reader_api(request):
    return handle_nvidia_raw_dataset_reader_request(request, client, generate_stream_responses)
    
@csrf_exempt
@require_http_methods(["POST"])
def nvidia_api_prompt_generator_ds_api(request):
    return handle_nvidia_api_prompt_generator_ds_request(request, client, generate_stream_responses)
    