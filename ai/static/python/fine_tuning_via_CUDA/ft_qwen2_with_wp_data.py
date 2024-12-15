import os
from datasets import load_dataset, concatenate_datasets
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
import torch

# Disable wandb
os.environ["WANDB_DISABLED"] = "true"
# To avoid fragmentation
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True" 


# Load the dataset
dataset = load_dataset("knkrn5/wealthpsychology-tokenized-data")

# Initialize model and tokenizer
model_name = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Handle tokenizer padding
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = model.config.eos_token_id

# Check CUDA availability
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=5e-5,
    per_device_eval_batch_size=2,  # Added eval batch size
    gradient_accumulation_steps=2,
    num_train_epochs=5,
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,
    save_total_limit=3,
    fp16=torch.cuda.is_available(),  # Only use fp16 if CUDA is available
    use_cpu=not torch.cuda.is_available(),  #to specify CPU usage
)

# Prepare datasets
def preprocess_function(examples):
    return {
        "input_ids": examples["input_ids"],
        "attention_mask": examples["attention_mask"]
    }

# Apply preprocessing
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Concatenate datasets
train_dataset = concatenate_datasets([
    tokenized_datasets["wp_pages"],
    tokenized_datasets["blog_categories"],
    tokenized_datasets["fin_calculators"],
    tokenized_datasets["fin_quizzes"]
])

eval_dataset = concatenate_datasets([
    tokenized_datasets["wp_home"],
    tokenized_datasets["contact_info"],
    tokenized_datasets["about_us"],
    tokenized_datasets["our_team"],
    tokenized_datasets["our_plan"]
])

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
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