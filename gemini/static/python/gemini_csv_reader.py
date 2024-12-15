import os
import google.generativeai as genai
from dotenv import load_dotenv
import csv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API"))

# Specify the model name
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

# Specify the file path
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

# Read the file content
# Function to extract text from CSV files
def extract_csv_text(csv_files):
    all_data = []  # List to store combined data from all files
    for csv_data in csv_files:
        try:
            with open(csv_data, 'r', encoding='utf-8') as file:
                csv_content = csv.DictReader(file)
                for row in csv_content:
                    all_data.append(row)
        except Exception as e:
            print(f"Error reading CSV file {csv_data}: {e}")
    
    return all_data  # Return combined data from all files

# Extract text from CSV files
csv_text = extract_csv_text(csv_files)

if not csv_text:
    print("Failed to extract text from the CSV. Please check the file paths and content.")
    exit()

print("\nCSV Text Extracted Successfully!")

csv_text_str = "\n".join([str(row) for row in csv_text])  # Convert list of dictionaries to a string
print(csv_text_str)


# Interactive question-answer loop
while True:
    user_question = input("\nPlease ask your question (or type 'exit' to quit): ")
    
    if user_question.lower() in ['exit', 'q']:
        print("Exiting...")
        break

    try:
        # Generate content using the text data as context
        prompt = (
            "You are a helpful assistant. Only answer questions based on the provided data. "
            "Do not answer any questions that are not based on the data. "
            f"Data:\n{csv_text}\n\n"
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
