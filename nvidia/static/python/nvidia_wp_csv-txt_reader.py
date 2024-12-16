import os
from dotenv import load_dotenv
from openai import OpenAI
import csv

# Load environment variables
load_dotenv()

# List to store rows as dictionaries
csv_files = ['static/data/wp-csv-data/wp-pages.csv', 
            'static/data/wp-csv-data/wp-home.csv', 
            'static/data/wp-csv-data/blog-categories.csv', 
            'static/data/wp-csv-data/fin-calculators.csv', 
            'static/data/wp-csv-data/fin-quizzes.csv', 
            'static/data/wp-csv-data/contact-info.csv', 
            'static/data/wp-csv-data/about-us.csv', 
            'static/data/wp-csv-data/our-team.csv', 
            'static/data/wp-csv-data/our-plan.csv'
            ]

text_file = "static/data/wp-txt-data/about-me.txt"

#model options
models = {
    "1": "nvidia/llama-3.1-nemotron-70b-instruct",
    "2": "meta/llama-3.3-70b-instruct",
    "3": "mistralai/mixtral-8x7b-instruct-v0.1",
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

# Function to extract text from CSV files
def extract_csv_text_data(csv_files, text_file):
    all_data = []  # List to store combined data from all files
    
    with open(text_file, 'r', encoding='utf-8') as textFile:    
        text_content = textFile.read()
    
    for csv_data in csv_files:
        try:
            with open(csv_data, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    all_data.append({
                        'csv_entry': row,
                        'text_content': text_content
                    })
        except Exception as e:
            print(f"Error reading CSV file {csv_data}: {e}")
    
    return all_data  # Return combined data from all files

# Extract text from CSV files
csv_txt_data = extract_csv_text_data(csv_files, text_file)

if not csv_txt_data:
    print("Failed to extract text from the CSV. Please check the file paths and content.")
    exit()

print("\nCSV Text Extracted Successfully!")

# Convert combined data to text format for the model
csv_text_data_str = "\n".join([str(row) for row in csv_txt_data])  # Convert list of dictionaries to a string

while True:
    # Take user input for the question
    user_question = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    # Exit the loop if the user types 'exit' or 'q'
    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    try:
        # Create a completion request with the user question and extracted CSV text as context
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Only answer based on the provided CSV data. Do not answer any questions that are not based on the CSV data."},
                {"role": "assistant", "content": "I will only answer questions only based on the provided CSV data."},
                {"role": "system", "content": f"CSV Data:\n{csv_text_data_str}"},
                {"role": "user", "content": user_question}
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

