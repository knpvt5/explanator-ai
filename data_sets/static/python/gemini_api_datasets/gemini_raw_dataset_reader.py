import os
import google.generativeai as genai
from dotenv import load_dotenv
from datasets import load_dataset
import pandas as pd

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API"))

# Specify the model name
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

# Load the dataset
dataset = load_dataset("knkrn5/wealthpsychology-raw-data", streaming=True)

# Checking if the data has the tokenized format
print(dataset)

all_data = []

# Print details of each split in the DatasetDict
for split_name, split_data in dataset.items():
    split_rows = [row for row in split_data]
    split_df = pd.DataFrame(split_rows)
    all_data.append(split_df)
    
print(split_df.head())
print(all_data)
print("\n" + "="*50 + "\n") #simple line separator
    
# Interactive question-answer loop
while True:
    user_question = input("\nPlease ask your question (or type 'exit' to quit): ")
    
    if user_question.lower() in ['exit', 'q']:
        print("Exiting...")
        break

    try:
        # Generate content using the text data as context
        prompt = (
            "You are a helpful assistant. Only answer questions based on the provided text data. "
            "Do not answer any questions that are not based on the text data. "
            f"Text Data:\n{all_data}\n\n"
            f"User's Question: {user_question}"
        )

        response = model.generate_content(
            contents=prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
            stream=True,
            tools=None,
            tool_config=None,
            request_options=None
        )
        # print(response.text)
        for chunk in response:
                print(chunk.text, end='')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")
