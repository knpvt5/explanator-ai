from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import csv

# Use more CPU threads if running on CPU
torch.set_num_threads(10)

# Specify the model name
model_name = "Qwen/Qwen2.5-1.5B-Instruct"

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Read external text data
file_paths = ["static/data/wp-csv-data/wp-pages.csv",
            "static/data/wp-csv-data/wp-home.csv",
            "static/data/wp-csv-data/blog-categories.csv",
            "static/data/wp-csv-data/fin-calculators.csv",
            "static/data/wp-csv-data/fin-quizzes.csv",
            "static/data/wp-csv-data/contact-info.csv",
            "static/data/wp-csv-data/about-us.csv",
            "static/data/wp-csv-data/our-team.csv",
            "static/data/wp-csv-data/our-plan.csv"]

all_data = []

for file_path in file_paths:
    with open(file_path, "r", encoding="utf-8") as file:
        all_data.append(file.read())

print("text read successfully")
# print("\n", all_data)
    
# Set the pad_token_id to avoid warnings
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
print(f"Using device: {device}")


while True:
    # Take user input
    user_input = input("Enter your prompt (or type 'exit' or 'q' to quit): ")
    if user_input.lower() in ["exit", 'q']:
        print("Exiting...")
        break

    # Combine document data with user input
    combined_input = f"Document: {all_data}\n\nQuestion: {user_input}"

    # Tokenize the combined input
    inputs = tokenizer(combined_input,
                        return_tensors="pt",
                        padding=True,
                        truncation=True,
                        max_length=1024).to(device)

    # Generate text based on the input
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=2048,
        temperature=0.5,
        # top_p=0.90,
        num_return_sequences=1, 
        pad_token_id=tokenizer.pad_token_id,  # Avoid warnings
        # repetition_penalty=1.2
    )

    # Decode and print the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Response: {generated_text}")
