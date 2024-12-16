import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
# print(os.getenv("NVIDIA_API")) 

#model options
models = {
    "1": "nvidia/llama-3.1-nemotron-70b-instruct",
    "2": "meta/llama-3.3-70b-instruct",
    "3": "mistralai/mixtral-8x7b-instruct-v0.1",
    "4": "nv-mistralai/mistral-nemo-12b-instruct",
    "5": "nvidia/nemotron-4-340b-instruct",
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
# print(os.getenv("NVIDIA_API")) 

while True:
    # Take user input for the question
    user_input = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    # Exit the loop if the user types 'exit'
    if user_input.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    # Create a completion request with the user question
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": " your are an AI assistant."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.5,
        # top_k = 50,
        top_p=0.7,
        max_tokens=512,
        # repetition_penalty=1.2,
        stream=True
    )

    # Stream the response chunks and print them
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")