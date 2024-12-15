import os
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API"))

# Specify the model name
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)


# Function to extract text from a PDF file
def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()  # Extract text from each page
    return text

# Ask for PDF file path and extract the text
pdf_path = "./data/economic.pdf"
pdf_text = extract_pdf_text(pdf_path)

print("\nPDF Text Extracted Successfully!")


# Interactive question-answer loop
while True:
    user_input = input("\nPlease ask your question (or type 'exit' to quit): ")
    
    if user_input.lower() in ['exit', 'q']:
        print("Exiting...")
        break

    try:
        # Generate content using the text data as context
        prompt = (
            "You are a helpful assistant. Only answer questions based on the provided data. "
            "Do not answer any questions that are not based on the data. "
            f"Text Data:\n{pdf_text}\n\n"
            f"User's Question: {user_input}"
        )
        

        response = model.generate_content(
            contents=prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
            stream=True,
        )
        # print(response.text)
        for chunk in response:
                print(chunk.text, end='')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")
