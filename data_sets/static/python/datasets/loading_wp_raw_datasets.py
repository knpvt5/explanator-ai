from datasets import load_dataset

# Load the dataset
dataset = load_dataset("knkrn5/wealthpsychology-raw-data")

# Check if the data has the tokenized format
print(dataset)
print(dataset["wp_pages"])  # To check one split
# print(dataset.column_names)

# Print details of each split in the DatasetDict
for split_name, split_data in dataset.items():
    print(f"Split: {split_name}")
    print(f"Number of rows: {split_data.num_rows}")
    print(f"Columns: {split_data.column_names}")
    print("Data Preview:")
    print(split_data.to_pandas())  # Convert to Pandas DataFrame for better visualization
    print("\n" + "="*50 + "\n")

