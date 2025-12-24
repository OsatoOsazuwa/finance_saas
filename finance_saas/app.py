import streamlit as st
import pandas as pd
from nlp_classify import classify_transactions
from forecast import forecast_income_expense
from dashboard import display_dashboard
from report import generate_pdf_report, generate_excel_report

st.title("Financial Summary SaaS")

uploaded_file = st.file_uploader("Upload your bank statements (CSV/Excel)", type=['csv','xlsx'], accept_multiple_files=True)

if uploaded_file:
    # Combine multiple files
    df_list = []
    for file in uploaded_file:
        if file.name.endswith('.csv'):
            df_list.append(pd.read_csv(file))
        else:
            df_list.append(pd.read_excel(file))
    df = pd.concat(df_list, ignore_index=True)

    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])

    st.subheader("Classifying Transactions...")
    df = classify_transactions(df, retrain=True)  # automatic retrain with new data
    st.success("Transactions classified successfully!")

    st.subheader("Forecasting...")
    forecast_results, accuracy_results = forecast_income_expense(df)
    st.write("Forecast Accuracy per Category:")
    st.write(accuracy_results)

    st.subheader("Dashboard")
    display_dashboard(df)

    st.subheader("Download Reports")
    pdf_data = generate_pdf_report(df, forecast_results)
    st.download_button("Download PDF Report", pdf_data, file_name="financial_report.pdf")
    excel_data = generate_excel_report(df, forecast_results)
    st.download_button("Download Excel Report", excel_data, file_name="financial_report.xlsx")
