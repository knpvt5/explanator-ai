import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

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


# Initialize the OpenAI client with NVIDIA's base URL and API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

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
json_text_str = "\n".join([str(row) for row in json_text])  # Convert list of dictionaries to a string

while True:
    # Take user input for the question
    user_input = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    # Exit the loop if the user types 'exit' or 'q'
    if user_input.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    try:
        # Create a completion request with the user question and extracted JSON text as context
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Only answer based on the provided JSON data. Do not answer any questions that are not based on the JSON data."},
                {"role": "assistant", "content": "I will only answer questions only based on the provided JSON data."},
                {"role": "system", "content": f"JSON Data:\n{json_text_str}"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            # repetition_penalty=1.2,
            stream=True
        )

        # Stream the response chunks and print them
        print("\nAI Response:")
        for chunk in completion:
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="")
        print()  # For newline after the streamed response

    except Exception as e:
        print(f"Error occurred during completion request: {e}")

