# NVIDIA API Chatbot and Gemini API Chatbot

The image compares the code implementation for chatbots built using NVIDIA's API and Google's Gemini API. Each chatbot is designed to utilize the respective model's capabilities for interactive AI-driven communication.

---

## **NVIDIA API Chatbot**

### **Overview**

- **Purpose**: Leverages NVIDIA's pre-trained large language models for conversational AI.
- **Features**:
  - **Model Selection**: Offers multiple models, such as LLaMA variants and Microsoft Phi.
  - **Environment Variable Integration**: Uses `.env` files for secure key management.
  - **API Usage**: Employs OpenAI's API to interact with the selected NVIDIA models.

### **Functionality**

1. Prompts the user to select from a list of available NVIDIA models.
2. Loads environment variables for configuration and secure API key access.
3. Processes user queries through the selected model and returns AI-generated responses.

---

## **Gemini API Chatbot**

### **Overview**

- **Purpose**: Utilizes Google’s Gemini generative AI for interactive chatbot functionality.
- **Features**:
  - **Generative AI Integration**: Connects to Gemini's API for advanced conversational capabilities.
  - **Safety Settings**: Configures parameters to ensure appropriate interactions.
  - **Continuous Interaction**: Runs in a loop, allowing users to input queries until they exit.

### **Functionality**

1. Configures the Gemini API with the provided environment variables.
2. Allows users to input queries continuously while offering an option to exit.
3. Applies safety settings to monitor and control chatbot behavior.

---

## **Key Differences**

- **NVIDIA API Chatbot**: Focuses on flexibility by providing multiple pre-trained models for various use cases.
- **Gemini API Chatbot**: Prioritizes user safety and smooth interaction through generative AI and safety configurations.

Both chatbots demonstrate the use of powerful APIs to deliver conversational experiences while ensuring security and scalability.
