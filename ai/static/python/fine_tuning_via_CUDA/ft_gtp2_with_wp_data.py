import os
from datasets import load_dataset, concatenate_datasets
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
import torch

# Load the dataset
dataset = load_dataset("knkrn5/wealthpsychology-tokenized-data")

# Check if the data has the tokenized format
print(dataset)

model_name = "gpt2" #similarly it can be fine-tuned with gpt2-xl, gpt2-medium, gpt2-large.

# Define the model
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

os.environ["WANDB_DISABLED"] = "true"

# Setting the pad_token_id to the eos_token_id to avoid warnings and errors
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# Move the model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"Using device: {device}")


# Define the training arguments
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=2,  # Reduced batch size
    gradient_accumulation_steps=2,  # Simulate larger batch size
    num_train_epochs=5,
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,
    save_total_limit=3,
    fp16=True,  # Mixed precision training
)


# Prepare the dataset
def preprocess_function(examples):
    return {
        "input_ids": examples["input_ids"],
        "attention_mask": examples["attention_mask"]
    }

# Apply the preprocessing function
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Concatenate datasets for training and evaluation
train_dataset = concatenate_datasets([tokenized_datasets["wp_pages"],
                                        tokenized_datasets["blog_categories"],
                                        tokenized_datasets["fin_calculators"],
                                        tokenized_datasets["fin_quizzes"]])

eval_dataset = concatenate_datasets([tokenized_datasets["wp_home"],
                                        tokenized_datasets["contact_info"],
                                        tokenized_datasets["about_us"],
                                        tokenized_datasets["our_team"],
                                        tokenized_datasets["our_plan"]])

# Define the data collator for language modeling (handles padding)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  # GPT-2 does not use masked language modeling
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,  # Use the data collator for padding
    tokenizer=tokenizer,
)

# Train the model
try:
    trainer.train()
    
    # Save the model
    output_dir = "./final_model"
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model saved to {output_dir}")
    
except Exception as e:
    print(f"An error occurred during training: {str(e)}")
