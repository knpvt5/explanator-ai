import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup 

load_dotenv()

urls = ["https://wealthpsychology.in/index.html",
        "https://wealthpsychology.in/blog/",
        "https://wealthpsychology.in/financial-calculators/",
        "https://wealthpsychology.in/finance-quizzes/",
        "https://wealthpsychology.in/contact-us/",
        "https://wealthpsychology.in/about-us/",
        "https://wealthpsychology.in/our-team/",
        "https://wealthpsychology.in/our-plans/"
    ]

all_data = []

genai.configure(api_key=os.getenv("GEMINI_API"))
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_all_text(urls):
    try:
        # Send a GET request to the URL
        for url in urls:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract all text
            text = soup.get_text(separator="\n")  # Separate text blocks with newlines
            # Remove extra newlines
            cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
            # Append cleaned text to the list
            all_data.append(cleaned_text)

        return "\n\n".join(all_data)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None

# calling function
extract_all_text(urls)
# print(website_data)
print(all_data)

print("Extracted Text successfully from the Website:")

while True:
    user_input = input("\nPlease ask your question (or type 'exit' to quit): ")
    
    if user_input.lower() in ['exit', 'q']:
        print("Exiting...")
        break

    try:
        # Generate content using the text data as context
        prompt = (
            "You are a helpful assistant. Only answer questions based on the provided text data. "
            "Do not answer any questions that are not based on the text data. "
            f"Site Data:\n{all_data}\n\n"
            f"User's Input: {user_input}"
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
            stream=True
            )
        for chunk in response:
                print(chunk.text, end='')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")