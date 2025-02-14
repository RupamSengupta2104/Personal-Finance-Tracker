import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load the cleaned dataset
file_path = Path("data/finance_data_cleaned.csv")
df = pd.read_csv(file_path)

# Convert 'Date' to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Display dataset summary
print(df.info())
print("\nSummary Statistics:\n", df.describe())
print("\nTransaction Categories:\n", df["Category"].value_counts())

# Calculate total income and expenses
total_income = df[df["Type"] == "Income"]["Amount"].sum()
total_expense = df[df["Type"] == "Expense"]["Amount"].sum()

print(f"\nTotal Income: ${total_income}")
print(f"Total Expenses: ${total_expense}")
print(f"Net Savings: ${total_income + total_expense}")

# Monthly Trends
df["Month"] = df["Date"].dt.to_period("M")
monthly_data = df.groupby(["Month", "Type"])["Amount"].sum().unstack()

plt.figure(figsize=(10, 5))
monthly_data.plot(kind="bar", stacked=True, colormap="coolwarm", figsize=(12, 6))
plt.xlabel("Month")
plt.ylabel("Total Amount ($)")
plt.title("Monthly Income vs. Expenses")
plt.xticks(rotation=45)
plt.legend(["Income", "Expenses"])
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("images/monthly_trend.png", bbox_inches="tight")

# Category-Wise Spending
expense_data = df[df["Type"] == "Expense"]

plt.figure(figsize=(10, 5))

# Fix: Assign `Category` to `hue` and set `legend=False`
sns.barplot(
    data=expense_data, x="Category", y="Amount", hue="Category", 
    dodge=False, palette="Reds_r", legend=False
)

plt.xlabel("Spending Category")
plt.ylabel("Total Spent ($)")
plt.title("Total Spending by Category")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("images/category_spending.png", bbox_inches="tight")


print("\n Analysis complete! Visualizations saved in 'images' folder.")
