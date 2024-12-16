import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

#model options
models = {
    "1": "nvidia/llama-3.1-nemotron-70b-instruct",
    "2": "meta/llama-3.3-70b-instruct",
    # "3": "mistralai/mixtral-8x7b-instruct-v0.1",
    "4": "nv-mistralai/mistral-nemo-12b-instruct",
    # "5": "nvidia/nemotron-4-340b-instruct",
}

# Prompt user to select a model
print("Select a model:")
for key, value in models.items():
    print(f"{key}. {value}")

# Validate user input in a loop
while True:
    model_choice = input("\nEnter the number corresponding to the model: ")
    if model_choice in models:
        model_name = models[model_choice]
        break
    else:
        print("Invalid choice. Please enter a valid number.")

print("Using model:", model_name)

# Initialize the OpenAI client with NVIDIA's base URL and API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

# txt docs path
txt_path = "./static/data/wp-txt-data/about-me.txt"

# Open the file in read mode ('r')
with open(txt_path, 'r', encoding='utf-8') as file:
    # Read the entire content of the file
    txt_content = file.read()
print("Text read successfully.")
print(f"Analyzing text with length: {len(txt_content)}")

if not txt_content:
    print("Failed to extract text from the txt. Please check the file path and content.")
    exit()

while True:
    # Take user input for the question
    user_question = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    # Exit the loop if the user types 'exit'
    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    # Create a completion request with the user question
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant. Only answer questions using the following text data. Do not use outside knowledge."},
            {"role": "assistant", "content": "I will answer questions only based on the provided text data."},
            {"role": "system", "content": f"Text Data:\n{txt_content}"},
            {"role": "user", "content": user_question}
        ],
        temperature=0.5,
        top_p=0.7,
        max_tokens=1024,
        # repetition_penalty=1.2,
        stream=True
    )

    # Stream the response chunks and print them
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
