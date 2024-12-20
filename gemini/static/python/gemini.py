import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API"))
model = genai.GenerativeModel("gemini-1.5-flash")

while True:
    user_input = input("\nPlease ask your question (or type 'exit' to quit): ")
    
    if user_input.lower() in ['exit', 'q']:
        print("Exiting...")
        exit()

    # Define safety settings
    safety_settings = [
        {
            "category": "HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        # {
        #     "category": "DANGEROUS_CONTENT",
        #     "threshold": "BLOCK_NONE",
        # },
    ]

    try:
        response = model.generate_content(
            user_input,
            generation_config=genai.types.GenerationConfig(max_output_tokens=1024),
            safety_settings=safety_settings,
            stream=True
            )
        for chunk in response:
                print(chunk.text, end='')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or check your API key and internet connection.")