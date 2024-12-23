import os
from dotenv import load_dotenv
from openai import OpenAI
from datasets import load_dataset
import pandas as pd

load_dotenv()

# Loading dataset in streaming mode
dataset = load_dataset("knkrn5/wealthpsychology-raw-data", streaming=True)

# Printing whole dataset
# print(dataset)

all_data = []

# Processing each split in the dataset
for split_name, split_data in dataset.items():
    split_rows = [row for row in split_data]
    split_df = pd.DataFrame(split_rows)
    all_data.append(split_df)

# print(f"Split: {split_name}")
# print(split_df.head())

models = {
    "1": "nvidia/llama-3.1-nemotron-70b-instruct",
    "2": "meta/llama-3.3-70b-instruct",
    # "3": "mistralai/mixtral-8x7b-instruct-v0.1",
    "4": "nv-mistralai/mistral-nemo-12b-instruct",
    # "5": "mistralai/mixtral-8x22b-instruct-v0.1",
    # "6": "nvidia/nemotron-4-340b-instruct",
    "7": "microsoft/phi-3-mini-128k-instruct",
}

#select  model
print("Select a model:")
for key, value in models.items():
    print(f"{key}. {value}")

while True:
    model_choice = input("\nEnter the number corresponding to the model: ")
    if model_choice in models:
        model_name = models[model_choice]
        break
    else:
        print("Invalid choice. Please enter a valid number.")

print("Using model:", model_name)

# OpenAI client Init
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

while True:
    # user input 
    user_input = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    if user_input.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    # completion
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "system", "content": f"Dataset: {all_data}."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.5,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )

    # Streaming response 
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
