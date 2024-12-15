from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from tqdm import tqdm  # Import tqdm for progress bar

# Use more CPU threads if running on CPU
torch.set_num_threads(8)  

# Load the pre-trained GPT-2 model and tokenizer
model_name = 'gpt2-xl'  
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Setting the pad_token_id to the eos_token_id to avoid warnings and errors
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
print(f"Using device: {device}")

while True:
    user_question = input("Please ask a question or type 'exit' or 'q' to exit: ")
    if user_question.lower() == "exit" or user_question.lower() == "q":
        print("Exiting...")
        break

    # Tokenize user input and move tensors to the correct device
    inputs = tokenizer(user_question,
                        return_tensors="pt",
                        padding=True).to(device)

    # Display progress bar while generating response
    print("Processing...")

    # Create a tqdm progress bar, simulating a small task
    for _ in tqdm(range(1), desc="Generating Response", ncols=100):
        
        # Generate the output
        outputs = model.generate(
            inputs['input_ids'], 
            attention_mask=inputs['attention_mask'],  # Set attention mask here
            max_length=100,
            repetition_penalty=1.2,
            pad_token_id=model.config.pad_token_id  # Set pad_token_id here
        )

    # Decode and print the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Generated Response:", generated_text)
