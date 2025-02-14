import pandas as pd
from pathlib import Path

# Define file path
file_path = Path("data/finance_data.csv")

# Step 1: Load the dataset
df = pd.read_csv(file_path)

# Step 2: Check for missing values
print("Missing Values Before Cleaning:\n", df.isnull().sum())

# Step 3: Convert 'Date' column to datetime format
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # Convert, handling errors

# Step 4: Fill missing values in 'Category' and 'Description'
df = df.fillna({"Category": "Unknown", "Description": "No Description"})

# Step 5: Remove rows where 'Amount' is missing
df = df.dropna(subset=["Amount"])

# Step 6: Verify missing values after cleaning
print("\nMissing Values After Cleaning:\n", df.isnull().sum())

# Step 7: Save the cleaned data
cleaned_file_path = Path("data/finance_data_cleaned.csv")
df.to_csv(cleaned_file_path, index=False)

print("\n Data cleaning complete. Cleaned data saved to 'data/finance_data_cleaned.csv'")
