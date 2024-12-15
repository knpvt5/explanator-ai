from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from tqdm import tqdm 

# Set the number of CPU threads if running on CPU
torch.set_num_threads(10)

# Specify the model name
model_name = "facebook/opt-1.3b"

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set the pad_token_id to avoid warnings
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

while True:
    # Take user input
    user_input = input("Enter your prompt (or type 'exit' or 'q' to quit): ")
    if user_input.lower() in ["exit", 'q']:
        print("Exiting...")
        break

    # Tokenize the input
    inputs = tokenizer(user_input,
                        return_tensors="pt",
                        padding=True).to(device)
    
    # Display progress bar while generating response
    print("Processing...")

    # Create a tqdm progress bar, simulating a small task
    for _ in tqdm(range(1), desc="Generating Response", ncols=100):
        

        # Generate text based on the input
        outputs = model.generate(
            inputs['input_ids'],
            attention_mask=inputs['attention_mask'],  # Add attention mask
            max_length=200,  # Adjust max_length as needed
            temperature=0.5,  # Control randomness of the output
            do_sample=True,
            num_return_sequences=1,  # Number of responses to generate
            pad_token_id=tokenizer.pad_token_id,  # Avoid warnings
        )

    # Decode and print the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Response: {generated_text}")
