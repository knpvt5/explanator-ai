import os
import pandas as pd
from datasets import Dataset, DatasetDict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load all CSV files into DataFrames
wp_pages_df = pd.read_csv('data/wp-csv-data/wp-pages.csv')
wp_home_df = pd.read_csv('data/wp-csv-data/wp-home.csv')
blog_categories_df = pd.read_csv('data/wp-csv-data/blog-categories.csv')
fin_calculators_df = pd.read_csv('data/wp-csv-data/fin-calculators.csv')
fin_quizzes_df = pd.read_csv('data/wp-csv-data/fin-quizzes.csv')
contact_info_df = pd.read_csv('data/wp-csv-data/contact-info.csv')
about_us_df = pd.read_csv('data/wp-csv-data/about-us.csv')
our_team_df = pd.read_csv('data/wp-csv-data/our-team.csv')
our_plan_df = pd.read_csv('data/wp-csv-data/our-plan.csv')

# Function to standardize DataFrame structure
def standardize_dataframe(df, required_columns=['topic', 'description']):
    # Create missing columns with empty strings if they don't exist
    for col in required_columns:
        if col not in df.columns:
            df[col] = ''
    
    # Ensure only required columns are present and in the correct order
    return df[required_columns]


# Dictionary mapping original column names to standardized names
""" column_mappings = {
    # Default mappings for standard columns
    'modules': 'topic',
    'modules content': 'description',
    'blog categories': 'topic',
    'category': 'topic',
    'link': 'description',
    'calculator': 'topic',
    'calculator_link': 'description',
    'quiz': 'topic',
    'quiz_link': 'description',
    'contact': 'topic',
    'contact_link': 'description',
    'about': 'topic',
    'about_link': 'description',
    'team': 'topic',
    'team_link': 'description',
    'plan': 'topic',
    'plan_link': 'description'
}
"""

# Rename and standardize all dataframes
dataframes = {
    'wp_pages': wp_pages_df.rename(columns={'wp nav': 'topic', 'wp nav_link': 'description'}),
    'wp_home': wp_home_df.rename(columns={'modules': 'topic', 'modules content': 'description'}),
    'blog_categories': blog_categories_df.rename(columns={'blog categories': 'topic', 'wp nav_link': 'description'}),
    'fin_calculators': fin_calculators_df.rename(columns={'financial calculator name': 'topic', 'financials calculators links': 'description'}),
    'fin_quizzes': fin_quizzes_df.rename(columns={'financial quizzes': 'topic', 'financial quizzes_link': 'description'}),
    'contact_info': contact_info_df.rename(columns={'Contact information Type': 'topic', 'Email': 'description'}),
    'about_us': about_us_df.rename(columns={'about us': 'topic', 'description': 'description'}),
    'our_team': our_team_df.rename(columns={'Our team': 'topic', 'description': 'description'}),
    'our_plan': our_plan_df.rename(columns={'Topic': 'topic', 'Category': 'description'})
}

# Standardize all dataframes
standardized_dataframes = {
    name: standardize_dataframe(df) 
    for name, df in dataframes.items()
}

# Add this before pushing to verify all DataFrames are properly standardized
print("\nVerifying standardized DataFrames:")
for name, df in standardized_dataframes.items():
    print(f"\n{name} columns:", df.columns.tolist())
    print(f"{name} shape:", df.shape)
    print(f"First few rows:")
    print(df.head())

# Create a Hugging Face DatasetDict with standardized features
non_tokenized_data = DatasetDict({
    name: Dataset.from_pandas(df)
    for name, df in standardized_dataframes.items()
})

# Print dataset info for verification
print("Dataset structure:")
print(non_tokenized_data)
print("\nSample data from wp_pages:")
# print(standardized_dataframes['wp_pages'].head())

# Print the first few rows of all DataFrames
print("wp_pages_df:")
print(wp_pages_df.head(), "\n")

print("wp_home_df:")
print(wp_home_df.head(), "\n")

print("blog_categories_df:")
print(blog_categories_df.head(), "\n")

print("fin_calculators_df:")
print(fin_calculators_df.head(), "\n")

print("fin_quizzes_df:")
print(fin_quizzes_df.head(), "\n")

print("contact_info_df:")
print(contact_info_df.head(), "\n")

print("about_us_df:")
print(about_us_df.head(), "\n")

print("our_team_df:")
print(our_team_df.head(), "\n")

print("our_plan_df:")
print(our_plan_df.head(), "\n")



# Push the dataset to the Hugging Face Hub
# DATASET_NAME = "wealthpsychology-raw-data"
""" DATASET_NAME = "knkrn5/wealthpsychology-raw-data"
DESCRIPTION = "This dataset contains raw data for the Wealth Psychology website content."

non_tokenized_data.push_to_hub(
    repo_id=DATASET_NAME,
    private=False,
    token=os.getenv("HUGGING_FACE_WRITE_API"),
) """

from huggingface_hub import delete_repo

def push_dataset_with_overwrite(dataset_dict, repo_id, token):
    try:
        # First, delete the existing repository
        delete_repo(
            repo_id=repo_id,
            token=token,
            repo_type="dataset"
        )
        print(f"Successfully deleted existing dataset: {repo_id}")
    except Exception as e:
        print(f"Repository doesn't exist or error in deletion: {str(e)}")
    
    try:
        # Then push the new version
        dataset_dict.push_to_hub(
            repo_id=repo_id,
            private=False,
            token=token
        )
        print(f"Successfully pushed new version of dataset: {repo_id}")
    except Exception as e:
        print(f"Error pushing dataset: {str(e)}")

# Your existing data processing code remains the same until the push part...

# Replace the push_to_hub call with this:
DATASET_NAME = "knkrn5/wealthpsychology-raw-data"
DESCRIPTION = "This dataset contains raw data for the Wealth Psychology website content."

# Use the new function to push with overwrite
push_dataset_with_overwrite(
    dataset_dict=non_tokenized_data,
    repo_id=DATASET_NAME,
    token=os.getenv("HUGGING_FACE_WRITE_API")
)