import os
import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer
from dotenv import load_dotenv

load_dotenv()

# Load all CSV files into DataFrames (ensure the paths are correct)
wp_pages_df = pd.read_csv('wp-csv-data/wp-pages.csv')
wp_home_df = pd.read_csv('wp-csv-data/wp-home.csv')
blog_categories_df = pd.read_csv('wp-csv-data/blog-categories.csv')
fin_calculators_df = pd.read_csv('wp-csv-data/fin-calculators.csv')
fin_quizzes_df = pd.read_csv('wp-csv-data/fin-quizzes.csv')
contact_info_df = pd.read_csv('wp-csv-data/contact-info.csv')
about_us_df = pd.read_csv('wp-csv-data/about-us.csv')
our_team_df = pd.read_csv('wp-csv-data/our-team.csv')
our_plan_df = pd.read_csv('wp-csv-data/our-plan.csv')

# Define the tokenizer (you can use any model like GPT-2, BERT, allenai/longformer-large-4096 etc.)
tokenizer = AutoTokenizer.from_pretrained("allenai/longformer-large-4096")

# Set eos_token as pad_token
# tokenizer.pad_token = tokenizer.eos_token

# Function to tokenize the text in a DataFrame column (after concatenating multiple columns)
def tokenize_data(df, text_columns):
    # Concatenate the selected columns into a single string for each row
    text_data = df[text_columns].apply(lambda row: ' '.join(row.astype(str)), axis=1)
    
    # Initialize lists to store tokenized data
    input_ids = []
    attention_mask = []
    
    for text in text_data.tolist():
        # Tokenize with truncation, and check for overflowing tokens
        tokenized = tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=4000,
            return_overflowing_tokens=True
        )
        
        # Combine the main tokens and any overflowing tokens
        full_input_ids = tokenized["input_ids"][0]
        for overflow in tokenized.get("overflowing", []):
            full_input_ids.extend(overflow)
        
        # Add to the lists
        input_ids.append(full_input_ids)
        attention_mask.append([1] * len(full_input_ids))  # Adjust attention mask to match full tokens
    
    # Return the full tokenized result
    return {"input_ids": input_ids, "attention_mask": attention_mask}

# Tokenize each DataFrame by passing the required columns as a list
wealthpsychology_pages_tokenized = tokenize_data(wp_pages_df, ['wp nav', 'wp nav_link'])
wp_home_tokenized = tokenize_data(wp_home_df, ['modules', 'modules content'])
blog_categories_tokenized = tokenize_data(blog_categories_df, ['blog categories'])
fin_calculators_tokenized = tokenize_data(fin_calculators_df, ['financial calculator name', 'financials calculators links'])
fin_quizzes_tokenized = tokenize_data(fin_quizzes_df, ['financial quizzes', 'financial quizzes_link'])
contact_info_tokenized = tokenize_data(contact_info_df, ['Contact information Type', 'Email'])
about_us_tokenized = tokenize_data(about_us_df, ['about us', 'description'])
our_team_tokenized = tokenize_data(our_team_df, ['Our team', 'description'])
our_plan_tokenized = tokenize_data(our_plan_df, ['Category', 'Topic'])

# Combine them into a DatasetDict for easy access
tokenized_data = DatasetDict({
    'wp_pages': Dataset.from_dict(wealthpsychology_pages_tokenized),
    'wp_home': Dataset.from_dict(wp_home_tokenized),
    'blog_categories': Dataset.from_dict(blog_categories_tokenized),
    'fin_calculators': Dataset.from_dict(fin_calculators_tokenized),
    'fin_quizzes': Dataset.from_dict(fin_quizzes_tokenized),
    'contact_info': Dataset.from_dict(contact_info_tokenized),
    'about_us': Dataset.from_dict(about_us_tokenized),
    'our_team': Dataset.from_dict(our_team_tokenized),
    'our_plan': Dataset.from_dict(our_plan_tokenized)
})

# Check tokenized data
print(tokenized_data)
print(wealthpsychology_pages_tokenized["input_ids"][0])  # Full input IDs
print(wealthpsychology_pages_tokenized["attention_mask"][0])  # Attention mask 

decoded_text = tokenizer.decode(wealthpsychology_pages_tokenized["input_ids"][0], skip_special_tokens=True)
decoded_text = tokenizer.decode(wp_home_tokenized["input_ids"][0], skip_special_tokens=True)
decoded_text = tokenizer.decode(about_us_tokenized["input_ids"][0], skip_special_tokens=True)
decoded_text = tokenizer.decode(our_team_tokenized["input_ids"][0], skip_special_tokens=True)
print(decoded_text)



#for pushing dataset in hugging-face
""" DATASET_NAME = "wealthpsychology-tokenized-data"
DESCRIPTION = "This dataset contains tokenized data for Wealth Psychology website content, tokenized using Longformer tokenizer."

# Push the dataset to the Hugging Face Hub
tokenized_data.push_to_hub(
    repo_id=DATASET_NAME, 
    # repo_id="knkrn5/your_dataset_name", 
    private=False,         
    token=os.getenv("HUGGING_FACE_WRITE_API")  
) """

