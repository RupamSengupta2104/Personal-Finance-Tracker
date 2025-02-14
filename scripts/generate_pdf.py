from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import matplotlib.pyplot as plt

def create_pdf_report(dataframe, filename="financial_report.pdf"):
    """Generates a financial summary PDF report."""
    
    # Create a new PDF canvas
    pdf = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 50, "Personal Finance Report")
    
    # Summary Metrics
    total_income = dataframe[dataframe["Type"] == "Income"]["Amount"].sum()
    total_expense = dataframe[dataframe["Type"] == "Expense"]["Amount"].sum()
    net_savings = total_income - total_expense

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 100, f"💵 Total Income: ${total_income:,.2f}")
    pdf.drawString(100, height - 120, f"💸 Total Expenses: ${abs(total_expense):,.2f}")
    pdf.drawString(100, height - 140, f"💰 Net Savings: ${net_savings:,.2f}")
    
    # Save PDF
    pdf.save()
    print(f"✅ PDF report saved as {filename}")

# Example usage
if __name__ == "__main__":
    df = pd.read_csv("data/finance_data_cleaned.csv")  # Load dataset
    create_pdf_report(df)
