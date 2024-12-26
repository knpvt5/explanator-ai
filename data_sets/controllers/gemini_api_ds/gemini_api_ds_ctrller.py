import os
import google.generativeai as genai
from django.http import StreamingHttpResponse, JsonResponse
from datasets import load_dataset
import json
import pandas as pd
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def handle_gemini_raw_dataset_reader_request(request, model, generate_stream_responses): 
        # Load the dataset
    dataset = load_dataset("knkrn5/wealthpsychology-raw-data", streaming=True)

    # printing whole dataset
    # print(dataset)

    all_data = []

    # Print details of each split in the DatasetDict
    for split_name, split_data in dataset.items():
        split_rows = [row for row in split_data]
        split_df = pd.DataFrame(split_rows)
        all_data.append(split_df)
        
    """ print(split_df.head())
    print(all_data)
    print("\n" + "="*50 + "\n") """ 
    

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


def handle_gemini_api_prompt_generator_ds_request(request, model, generate_stream_responses): 
    try:
        body = json.loads(request.body.decode("utf-8"))
        user_input = body.get("userInput")

        # Loading dataset via HF in streaming mode
        dataset = load_dataset("fka/awesome-chatgpt-prompts", streaming=True)

        # logging.info("printing whole dataset","dataset")

        #to store the data
        data = []

        # Looping dataset
        for prompts in dataset['train']:
            data.append(f"{prompts}\n")

        # Joining list into a single str
        all_data = "".join(data)

        # logging.info(all_data)
            
        try:
            prompt = (
            "You are a professional prompt engineer. "
            "You will assist you in crafting prompts for ChatGPT and other AI models. "
            f"Dataset:\n{all_data}\n\n"
            f"User's Input: {user_input}"
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
            logging.error("Please try again or check your API key and internet connection.")
            return JsonResponse(f"An error occurred: {str(e)}")
                
    except Exception as e:
        return JsonResponse(f"An error occurred. Please try again or check Later.: {str(e)}")

