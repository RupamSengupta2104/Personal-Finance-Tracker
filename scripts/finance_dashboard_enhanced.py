import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Load the cleaned dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/finance_data_cleaned.csv")

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Transactions")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime(df["Date"]).min())
end_date = st.sidebar.date_input("End Date", pd.to_datetime(df["Date"]).max())
category = st.sidebar.multiselect("Select Categories", df["Category"].unique(), default=df["Category"].unique())

# Apply Filters
filtered_df = df[
    (pd.to_datetime(df["Date"]) >= pd.to_datetime(start_date)) &
    (pd.to_datetime(df["Date"]) <= pd.to_datetime(end_date)) &
    (df["Category"].isin(category))
]

# Calculate Metrics
total_income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
total_expense = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
net_savings = total_income - total_expense

# Layout with Columns
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.metric("💵 Total Income ($)", f"{total_income:,.2f}")

with col2:
    st.metric("💸 Total Expenses ($)", f"{abs(total_expense):,.2f}")

with col3:
    st.metric("💰 Net Savings ($)", f"{net_savings:,.2f}")

# Income & Expense Trends
st.subheader("📊 Monthly Income & Expense Trends")
df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")
monthly_summary = df.groupby(["Month", "Type"])["Amount"].sum().reset_index()
monthly_summary["Month"] = monthly_summary["Month"].astype(str)

fig = px.line(monthly_summary, x="Month", y="Amount", color="Type", markers=True, title="Income vs Expenses Over Time")
st.plotly_chart(fig, use_container_width=True)

# Category-wise Spending
st.subheader("📌 Category-wise Spending")
expense_data = filtered_df[filtered_df["Type"] == "Expense"]
fig_bar = px.bar(expense_data, x="Category", y="Amount", color="Category", title="Expenses by Category", text_auto=True)
st.plotly_chart(fig_bar, use_container_width=True)

# Download Transactions as CSV
def convert_df_to_csv(df):
    output = io.StringIO()
    df.to_csv(output, index=False)
    processed_data = output.getvalue()
    return processed_data

csv_data = convert_df_to_csv(filtered_df)
st.download_button(
    label="📥 Download Transactions as CSV",
    data=csv_data,
    file_name="filtered_transactions.csv",
    mime="text/csv"
)

# Savings Goal Tracker
st.sidebar.header("💰 Set Your Savings Goal")
savings_goal = st.sidebar.number_input("Enter your savings goal ($)", min_value=0.0, value=1000.0)

progress = (net_savings / savings_goal) * 100 if savings_goal else 0
progress = min(progress, 100)

st.sidebar.progress(progress / 100)
st.sidebar.write(f"**Progress: {progress:.2f}%** of your goal")

# Display Filtered Transactions
st.subheader("📋 Filtered Transactions")
st.dataframe(filtered_df)

