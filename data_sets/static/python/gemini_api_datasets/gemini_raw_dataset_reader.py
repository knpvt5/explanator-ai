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

# Loading dataset
dataset = load_dataset("knkrn5/wealthpsychology-raw-data", streaming=True)

print(dataset)

all_data = []

# each split in the DatasetDict
for split_name, split_data in dataset.items():
    split_rows = [row for row in split_data]
    split_df = pd.DataFrame(split_rows)
    all_data.append(split_df)
    
print(split_df.head())
print(all_data)
print("\n" + "="*50 + "\n") 
    
    
while True:
    # user input
    user_input = input("\nPlease ask your question (or type 'exit' to quit): ")
    
    if user_input.lower() in ['exit', 'q']:
        print("Exiting...")
        break

    try:
        prompt = (
            "You are a helpful assistant. Only answer questions based on the provided dataset. "
            "Do not answer any questions that are not based on the dataset. "
            f"Dataset:\n{all_data}\n\n"
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
        
        for chunk in response:
                print(chunk.text, end='')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")
