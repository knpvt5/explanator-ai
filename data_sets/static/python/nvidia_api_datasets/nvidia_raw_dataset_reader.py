import os
from dotenv import load_dotenv
from openai import OpenAI
from datasets import load_dataset
import pandas as pd

load_dotenv()

# Load the dataset in streaming mode
dataset = load_dataset("knkrn5/wealthpsychology-raw-data", streaming=True)

# Checking the dataset details
print(dataset)

all_data = []

# Process each split in the dataset
for split_name, split_data in dataset.items():
    split_rows = [row for row in split_data]
    split_df = pd.DataFrame(split_rows)
    all_data.append(split_df)

# Print details of the DataFrame
print(f"Split: {split_name}")
print(split_df.head())
print("\n" + "="*50 + "\n")

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

while True:
    # Take user input for the question
    user_question = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    # Exit the loop if the user types 'exit'
    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    # Create a completion request with the user question
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "system", "content": f"Dataset: {all_data}."},
            {"role": "user", "content": user_question}
        ],
        temperature=0.5,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )

    # Stream the response chunks and print them
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
