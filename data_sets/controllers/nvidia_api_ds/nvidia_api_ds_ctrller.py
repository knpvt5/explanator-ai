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
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(message)s - %(name)s -%(asctime)s '
)
# Initialize logging
logger = logging.getLogger(__name__)


def handle_nvidia_raw_dataset_reader_request(request, client, generate_stream_responses):
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

    # Printing details of the DataFrame
    """ print(f"Split: {split_name}")
    print(split_df.head()) """

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
            stream=True
        )
        
        # return JsonResponse({"response": completion.choices[0].message.content})
        response =  StreamingHttpResponse(generate_stream_responses(completion), content_type="text/even-steam")
        response['Cache-Control'] = 'no-cache'
        return response

    except Exception as e:
        logging.error(f"Error occurred during completion request: {e}")
        
        
        
def handle_nvidia_api_prompt_generator_ds_request(request, client, generate_stream_responses):
    try: 
        body  = json.loads(request.body.decode("utf-8"))
        user_input = body.get('userInput')
        model_name = body.get('modelName')
        
        if not model_name:
            model_name = "nvidia/llama-3.1-nemotron-70b-instruct"

        dataset = load_dataset("fka/awesome-chatgpt-prompts", streaming=True)
        data = []

        # Looping dataset
        for example in dataset['train']:
            data.append(f"{example}\n")

        # Joining list into a single str
        all_data = "".join(data)
        print(all_data)

        #openai completion
        completion = client.chat.completions.create(
            model= model_name,
            messages=[
                {"role": "system", "content": "You are a professional prompt engineer."}, 
                {"role": "assistant", "content": "I will assist you in crafting prompts for ChatGPT and other AI models."},
                {"role": "system", "content": f"dataset: {all_data}."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            # top_k = 50,
            top_p=0.7,
            max_tokens=2048,
            # repetition_penalty=1.2,
            stream=True
        )

        # Streaming responses
        return StreamingHttpResponse(generate_stream_responses(completion), content_type="text/event-stream")

    
    except json.decoder.JSONDecodeError as e:
        logging.error(f"Error occurred while decoding JSON: {e}") 
            
    except Exception as e:
        logging.error(f"Error occurred during completion request: {e}")     
