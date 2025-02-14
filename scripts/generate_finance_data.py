import pandas as pd
from pathlib import Path

# Define the file path using pathlib
data_folder = Path("data")
file_path = data_folder / "finance_data.csv"

# Ensure the data folder exists
data_folder.mkdir(parents=True, exist_ok=True)

# Create sample finance data
data = {
    "Date": [
        "2025-02-01", "2025-02-02", "2025-02-05", "2025-02-07", "2025-02-10",
        "2025-02-15", "2025-02-18", "2025-02-20", "2025-02-22", "2025-02-25"
    ],
    "Category": [
        "Salary", "Groceries", "Rent", "Investment", "Entertainment",
        "Utilities", "Dining Out", "Shopping", "Transport", "Savings"
    ],
    "Amount": [5000, 200, 1000, 500, 100, 150, 50, 250, 80, 600],
    "Type": ["Income", "Expense", "Expense", "Income", "Expense",
             "Expense", "Expense", "Expense", "Expense", "Income"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save as CSV
df.to_csv(file_path, index=False)

print(f" Sample finance data saved to {file_path}")
