import os
from datasets import load_dataset, concatenate_datasets
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
import torch
import torch_xla.core.xla_model as xm
import torch_xla.distributed.xla_multiprocessing as xmp

def train_fn(index):
    # Load the dataset
    dataset = load_dataset("knkrn5/wealthpsychology-tokenized-data")

    model_name = "facebook/opt-1.3b"

    # Define the model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Set pad_token_id to eos_token_id to avoid warnings
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = model.config.eos_token_id

    # Move the model to TPU
    device = xm.xla_device()
    model.to(device)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",
        learning_rate=5e-5,
        gradient_accumulation_steps=8, 
        per_device_train_batch_size=4,  # TPU can handle larger batch sizes
        num_train_epochs=5,
        save_strategy="epoch",
        logging_dir="./logs",
        logging_steps=10,
        load_best_model_at_end=True,
        save_total_limit=3,
        fp16=False,  # Mixed precision is not supported on TPU
    )

    # Preprocessing
    def preprocess_function(examples):
        return {
            "input_ids": examples["input_ids"],
            "attention_mask": examples["attention_mask"]
        }

    # Apply preprocessing
    tokenized_datasets = dataset.map(preprocess_function, batched=True)

    # Concatenate datasets
    train_dataset = concatenate_datasets([tokenized_datasets["wp_pages"],
                                          tokenized_datasets["blog_categories"],
                                          tokenized_datasets["fin_calculators"],
                                          tokenized_datasets["fin_quizzes"]])

    eval_dataset = concatenate_datasets([tokenized_datasets["wp_home"],
                                         tokenized_datasets["contact_info"],
                                         tokenized_datasets["about_us"],
                                         tokenized_datasets["our_team"],
                                         tokenized_datasets["our_plan"]])

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    # Trainer setup
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )

    # Train the model
    trainer.train()

    # Save the model and tokenizer
    trainer.save_model("./final_model")
    tokenizer.save_pretrained("./final_model")


if __name__ == "__main__":
    os.environ["WANDB_DISABLED"] = "true"
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    xmp.spawn(train_fn, nprocs=1)  # Use 1 TPU core
