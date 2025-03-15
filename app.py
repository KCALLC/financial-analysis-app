import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def categorize_objt(objt):
    try:
        objt = int(objt)
        if 1000 <= objt <= 7999:
            return "Expenditures"
        elif 8000 <= objt <= 8999:
            return "Revenues"
        elif 9000 <= objt <= 9199:
            return "Cash"
        elif 9200 <= objt <= 9299:
            return "Accounts Receivable"
        elif objt == 9330:
            return "Prepaid Expenses"
        elif 9300 <= objt <= 9329 or 9331 <= objt <= 9399:
            return "Other Current Assets"
        elif 9400 <= objt <= 9499:
            return "Fixed Assets"
        elif 9500 <= objt <= 9501:
            return "Accounts Payable"
        elif 9502 <= objt <= 9599:
            return "Accrued Liabilities"
        elif objt == 9665:
            return "Comp Absences"
        elif objt == 9610:
            return "Intercompany Payables"
        elif objt == 9650:
            return "Deferred/Unearned Revenue"
        elif objt == 9640:
            return "Current Loans"
        elif 9500 <= objt <= 9699:
            return "Other Liabilities"
        elif 9700 <= objt <= 9799:
            return "Fund Balance"
        else:
            return "Other"
    except ValueError:
        return "Unknown"

def calculate_amount(row):
    return row.get("Debit", 0) - row.get("Credit", 0)

def process_file(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.rename(columns={"Code0SegNum": "Object"}, inplace=True)
    df["Account Category"] = df["Object"].apply(categorize_objt)
    df["Calculated Amount"] = df.apply(calculate_amount, axis=1)
    return df

def main():
    st.title("Financial Data Analyzer")
    st.write("Upload your financial CSV file to generate reports and visualizations.")
    
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = process_file(uploaded_file)
        st.write("### Processed Financial Data", df)
        
        balance_sheet_df = df[df["Account Category"].isin(["Cash", "Accounts Receivable", "Prepaid Expenses", "Other Current Assets", "Fixed Assets", "Accounts Payable", "Accrued Liabilities", "Comp Absences", "Intercompany Payables", "Deferred/Unearned Revenue", "Current Loans", "Other Liabilities", "Fund Balance"])].groupby("Account Category")["Calculated Amount"].sum().reset_index()
        
        total_assets = balance_sheet_df[balance_sheet_df["Account Category"].isin(["Cash", "Accounts Receivable", "Prepaid Expenses", "Other Current Assets", "Fixed Assets"])]
        total_liabilities = balance_sheet_df[balance_sheet_df["Account Category"].isin(["Accounts Payable", "Accrued Liabilities", "Comp Absences", "Intercompany Payables", "Deferred/Unearned Revenue", "Current Loans", "Other Liabilities"])]
        fund_balance = balance_sheet_df[balance_sheet_df["Account Category"] == "Fund Balance"]
        
        st.write("## Balance Sheet (Statement of Net Position)")
        st.dataframe(balance_sheet_df.style.format({"Calculated Amount": "${:,.0f}"}))
        
        st.write("**Total Assets: ${:,.0f}**".format(total_assets["Calculated Amount"].sum()))
        st.write("**Total Liabilities: ${:,.0f}**".format(total_liabilities["Calculated Amount"].sum()))
        st.write("**Ending Fund Balance: ${:,.0f}**".format(fund_balance["Calculated Amount"].sum()))
        st.write("**Liabilities + Fund Balance: ${:,.0f}**".format(total_liabilities["Calculated Amount"].sum() + fund_balance["Calculated Amount"].sum()))
        
        income_statement_df = df[df["Account Category"].isin(["Revenue", "Expenditure"])].groupby("Account Category")["Calculated Amount"].sum().reset_index()
        
        st.write("## Income Statement")
        st.dataframe(income_statement_df.style.format({"Calculated Amount": "${:,.0f}"}))
        
        if not income_statement_df.empty:
            st.write("## Revenue vs. Expenditure")
            fig, ax = plt.subplots()
            income_statement_df.plot(kind='bar', x="Account Category", y="Calculated Amount", ax=ax, legend=False)
            plt.ylabel("Amount ($)")
            plt.title("Revenue vs. Expenditure")
            plt.grid(axis="y")
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)
        else:
            st.warning("No income statement data available to plot.")

if __name__ == "__main__":
    main()
