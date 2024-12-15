import os
from dotenv import load_dotenv
from openai import OpenAI
from datasets import load_dataset

load_dotenv()

# Load the Hugging Face dataset
dataset = load_dataset("fka/awesome-chatgpt-prompts", streaming=True)

print(dataset)

# for i, example in enumerate(dataset['train']):

# Create a list to store the data
data = []

# Loop through the dataset
for example in dataset['train']:
    # Append each example as a string with a newline character
    data.append(f"{example}\n")

# Join the list into a single string with newline separators
all_data = "".join(data)

# Print the entire formatted data
print(all_data)


# Initialize the OpenAI client with NVIDIA's base URL and API key
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
            {"role": "system", "content": "You are a professional prompt engineer."}, 
            {"role": "assistant", "content": "I will assist you in crafting prompts for ChatGPT and other AI models."},
            {"role": "system", "content": f"dataset: {all_data}."},
            {"role": "user", "content": user_question}
        ],
        temperature=0.5,
        # top_k = 50,
        top_p=0.7,
        max_tokens=1024,
        # repetition_penalty=1.2,
        stream=True
    )

    # Stream the response chunks and print them
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
