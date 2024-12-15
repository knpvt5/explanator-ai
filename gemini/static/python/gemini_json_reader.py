import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API"))

# List to store rows as dictionaries
json_files = ['static/data/wp-json-data/wp-pages.json', 
            'static/data/wp-json-data/wp-home.json', 
            'static/data/wp-json-data/blog-categories.json', 
            'static/data/wp-json-data/fin-calculators.json', 
            'static/data/wp-json-data/fin-quizzes.json', 
            'static/data/wp-json-data/contact-info.json', 
            'static/data/wp-json-data/about-us.json', 
            'static/data/wp-json-data/our-team.json', 
            'static/data/wp-json-data/our-plan.json'
            ]

# Specify the model name
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

# Function to extract text from json files
def extract_json_text(json_files):
    all_data = []  # List to store combined data from all files
    for json_data in json_files:
        try:
            with open(json_data, 'r', encoding='utf-8') as jsonFile:
                reader = json.load(jsonFile) # Parse the JSON content as python dictionary
                for row in reader:
                    all_data.append(row)
        except Exception as e:
            print(f"Error reading JSON file {json_data}: {e}")
    
    return all_data  # Return combined data from all files

# Extract text from json files
json_text = extract_json_text(json_files)

if not json_text:
    print("Failed to extract text from the JSON. Please check the file paths and content.")
    exit()

print("\nJSON Text Extracted Successfully!")

# Convert combined data to text format for the model
json_text_str = "\n".join([str(row) for row in json_text])

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
            f"Text Data:\n{json_text_str}\n\n"
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
