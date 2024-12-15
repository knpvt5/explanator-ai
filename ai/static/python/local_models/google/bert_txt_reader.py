# Load model directly
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

#if running on CPU
torch.set_num_threads(100)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
model = AutoModelForMaskedLM.from_pretrained("google-bert/bert-base-uncased")


# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)


# Read document (context) from an external file
""" with open("data/document.txt", "r") as file:
    document = file.read() """

while True:
    
    # List of questions you want to ask
    user_input = input("\nAsk the question or type 'exit' or 'q' to quit: ")
    
    if user_input.lower() in ["exit", 'q']:
        print("Exiting...")
        break
    
        # Tokenize user input and move tensors to the correct device
    inputs = tokenizer(user_input, return_tensors="pt", padding=True).to(device)

    # Generate the output
    outputs = model.generate(
            inputs['input_ids'], 
            attention_mask=inputs['attention_mask'],  # Set attention mask here
            max_length=100,
            pad_token_id=model.config.pad_token_id  # Set pad_token_id here
        )

    # Decode and print the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Generated Response:", generated_text)
