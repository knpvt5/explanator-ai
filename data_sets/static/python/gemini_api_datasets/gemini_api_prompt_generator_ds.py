import os
import google.generativeai as genai
from dotenv import load_dotenv
from datasets import load_dataset
import pandas as pd

load_dotenv()

# Config Gemini API
genai.configure(api_key=os.getenv("GEMINI_API"))

# model name
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

# Loading dataset via HF in streaming mode
dataset = load_dataset("fka/awesome-chatgpt-prompts", streaming=True)

# print("printing whole dataset","dataset")

#to store the data
data = []

# Looping dataset
for prompts in dataset['train']:
    data.append(f"{prompts}\n")

# Joining list into a single str
all_data = "".join(data)

print(all_data)
    
    
while True:
    # user input
    user_input = input("\nPlease ask your question (or type 'exit' to quit): ")
    
    if user_input.lower() in ['exit', 'q']:
        print("Exiting...")
        break

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
        
        for chunk in response:
                print(chunk.text, end='')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")
