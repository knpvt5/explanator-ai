import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

#model options
models = {
    "1": "nvidia/llama-3.1-nemotron-70b-instruct",
    "2": "meta/llama-3.3-70b-instruct",
    "3": "mistralai/mixtral-8x7b-instruct-v0.1",
    "4": "nv-mistralai/mistral-nemo-12b-instruct",
    "5": "mistralai/mixtral-8x22b-instruct-v0.1",
    "6": "nvidia/nemotron-4-340b-instruct",
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


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)
# print(os.getenv("NVIDIA_API")) 

while True:
    # user input 
    user_input = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    if user_input.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    # Completion
    completion = client.chat.completions.create(
        model= model_name,
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

    # Streaming responses
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")