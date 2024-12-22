import os
from dotenv import load_dotenv
from openai import OpenAI
from datasets import load_dataset

load_dotenv()

# Load the Hugging Face dataset
dataset = load_dataset("fka/awesome-chatgpt-prompts", streaming=True)

# print(dataset)

# for i, example in enumerate(dataset['train']):

#to store the data
data = []

# Looping dataset
for example in dataset['train']:
    data.append(f"{example}\n")

# Join the list into a single str
all_data = "".join(data)

print(all_data)


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

while True:
    user_question = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    #openai completion
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

    # Streaming responses
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
