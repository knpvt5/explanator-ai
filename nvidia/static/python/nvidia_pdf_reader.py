import os
from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2

load_dotenv()

# print(f"Current Working Directory: {os.getcwd()}")

# Initialize the OpenAI client with NVIDIA's base URL and API key
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API")
)

# Function to extract text from a PDF file
def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()  # Extract text from each page
    return text

# Ask for PDF file path and extract the text
pdf_path = "./static/data/wp-pdf-data/wp.pdf"
pdf_text = extract_pdf_text(pdf_path)

print("\nPDF Text Extracted Successfully!")

while True:
    # Take user input for the question
    user_question = input("\nPlease enter your question (or type 'exit' or 'q' to quit): ")

    # Exit the loop if the user types 'exit' or 'quit'
    if user_question.lower() in ['exit', 'q']:
        print("Exiting the program.")
        break

    # Create a completion request with the user question and extracted PDF text as context
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": f"The content of the PDF is: {pdf_text[:20000]}..."},
            {"role": "user", "content": user_question}
        ],
        temperature=0.5,
        top_p=0.7,
        max_tokens=1024,
        # repetition_penalty=1.2,
        stream=True
    )

    # Stream the response chunks and print them
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
