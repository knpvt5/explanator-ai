# Chatbot APIs: NVIDIA and Gemini Integration

This documentation compares two chatbot implementations using different APIs: NVIDIA and Gemini. Both use Python and environment variables for API keys.

---

## NVIDIA API Chatbot

- **Libraries Used**:
  - `dotenv` to manage environment variables.
  - `openai` for accessing the NVIDIA chatbot API.
- **Steps**:
  1. Import the necessary libraries (`os`, `load_dotenv`, and `OpenAI`).
  2. Load the environment variables from the `.env` file.
  3. Initialize the OpenAI client using NVIDIA's base URL and API key.
  4. Start a while loop for continuous user input.
  5. If the user inputs a question, it is passed to the OpenAI model for processing.
  6. The API key is fetched using `os.getenv("NVIDIA_API")`.

---

## Gemini API Chatbot

- **Libraries Used**:
  - `dotenv` for environment management.
  - `google.generativeai` for connecting to the Gemini API.
- **Steps**:
  1. Import necessary libraries (`os`, `load_dotenv`, `generativeai`).
  2. Load environment variables.
  3. Initialize the Gemini model using the `genai.GenerativeModel` API.
  4. Define a function `ask_question()` to continuously prompt the user for input.
  5. The model responds based on user input or exits if the user types "exit" or "q".

---

## Key Notes

- The **NVIDIA API** integrates via OpenAI with the base URL `https://integrate.api.nvidia.com/v1`.
- The **Gemini API** connects through the `google.generativeai` library with the model `gemini-1.5-flash`.
- Both implementations use environment variables to securely store and retrieve API keys.

