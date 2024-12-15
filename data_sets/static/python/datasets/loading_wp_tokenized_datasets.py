from datasets import load_dataset
from transformers import AutoTokenizer
import pandas as pd

# Specify dataset and tokenizer
dataset_name = "knkrn5/wealthpsychology-tokenized-data"
tokenizer_name = "allenai/longformer-large-4096"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

# Load the tokenized dataset
dataset = load_dataset(dataset_name)
for split_name, split_data in dataset.items():
    print(f"Split: {split_name}")
    print(f"Columns: {split_data.column_names}")



""" # Decode the tokenized data and convert it to a Pandas DataFrame
def decode_and_convert_to_df(split_name, split_data):
    # Decode the tokenized 'input_ids' and preserve other columns
    decoded_data = split_data.map(
        lambda example: {
            "decoded_text": tokenizer.decode(example["input_ids"], skip_special_tokens=True),
            **{key: value for key, value in example.items() if key != "input_ids"}  # Keep other columns
        },
        remove_columns=["input_ids"],  # Remove 'input_ids' after decoding
    )
    # Convert to Pandas DataFrame
    return decoded_data.to_pandas()

# Process and display each split
for split_name, split_data in dataset.items():
    print(f"Processing split: {split_name}")
    split_df = decode_and_convert_to_df(split_name, split_data)
    print(f"Split: {split_name}")
    print(f"Number of rows: {len(split_df)}")
    print("Decoded Data Preview:")
    print(split_df.head())  # Show first few rows
    print("\n" + "=" * 50 + "\n") """
