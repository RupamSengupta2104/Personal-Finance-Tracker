import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# Set page title
st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")

# Load cleaned data
file_path = Path("data/finance_data_cleaned.csv")
df = pd.read_csv(file_path)

# Convert 'Date' to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Sidebar Filters
st.sidebar.header("Filter Transactions")
date_range = st.sidebar.date_input("Select Date Range", [df["Date"].min(), df["Date"].max()])
transaction_type = st.sidebar.selectbox("Select Transaction Type", ["All", "Income", "Expense"])
category = st.sidebar.multiselect("Select Category", options=df["Category"].unique(), default=df["Category"].unique())

# Apply filters
filtered_df = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]
if transaction_type != "All":
    filtered_df = filtered_df[filtered_df["Type"] == transaction_type]
filtered_df = filtered_df[filtered_df["Category"].isin(category)]

# Display DataFrame
st.dataframe(filtered_df)

# Total Income & Expense
total_income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
total_expense = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
net_savings = total_income + total_expense  # Expenses are negative

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Income ($)", f"{total_income:,.2f}")
col2.metric("Total Expenses ($)", f"{abs(total_expense):,.2f}")
col3.metric("Net Savings ($)", f"{net_savings:,.2f}")

# Monthly Income vs. Expense (Bar Chart)
df["Month"] = df["Date"].dt.to_period("M")
monthly_data = df.groupby(["Month", "Type"])["Amount"].sum().unstack().reset_index()
monthly_data["Month"] = monthly_data["Month"].astype(str)

fig = px.bar(monthly_data, x="Month", y=["Income", "Expense"], barmode="group", title="Monthly Income vs. Expenses")
st.plotly_chart(fig, use_container_width=True)

# Category-Wise Spending (Pie Chart)
expense_data = filtered_df[filtered_df["Type"] == "Expense"]
if not expense_data.empty:
    fig_pie = px.pie(expense_data, names="Category", values="Amount", title="Spending Breakdown by Category")
    st.plotly_chart(fig_pie, use_container_width=True)

st.success("✅ Dashboard Loaded Successfully!")
