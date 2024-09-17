import streamlit as st
import camelot
import pandas as pd
import os
import openpyxl
import matplotlib.pyplot as plt


def pdf_to_excel(uploaded_file):
    """Converts a PDF file to Excel.

    Args:
        uploaded_file (streamlit.UploadedFile): Contains information about the uploaded file.
    """

    if uploaded_file is not None:
        try:
            pdf_bytes = uploaded_file.getvalue()  # Get the file content as bytes
            with open("temp.pdf", "wb") as f:  # Write bytes to a temporary file
                f.write(pdf_bytes)
            pdf_file = "temp.pdf"  # Use the temporary file path

            # Check if the PDF file exists
            if not os.path.exists(pdf_file):
                raise FileNotFoundError(f"PDF file not found: {pdf_file}")

            tables = camelot.read_pdf(pdf_file, flavor='lattice')
            excel_file = pdf_file.replace(".pdf", ".xlsx")

            # Create an Excel writer
            writer = pd.ExcelWriter(excel_file, engine='openpyxl')

            # Write each table to a separate sheet
            for i, table in enumerate(tables):
                table.df.to_excel(writer, sheet_name=f"Table {i+1}")

            # Save the Excel file
            writer.close()

            # Download option
            with open(excel_file, "rb") as f:
                excel_data = f.read()
            st.download_button(
                label="Download Excel File",
                data=excel_data,
                file_name=excel_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success(f"PDF converted to Excel: {excel_file}")
            return excel_file  # Return the excel filename for further processing
        except Exception as e:
            st.error(f"Error converting PDF: {e}")
            return None  # Return None on error
        finally:
            # Remove the temporary file if it exists
            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")


def analyze_excel(excel_file):
    """
    Analyzes the uploaded Excel file and generates charts.

    Args:
        excel_file (str): Path to the Excel file.
    """

    if not excel_file:
        return

    # Load the Excel data using pandas
    df = pd.read_excel(excel_file)

    # Assuming your data has columns like "Bank", "Amount", and "Layer"
    # Modify these column names based on your actual data

    # Bank base (Top N)
    top_banks = df['Bank'].value_counts().nlargest(5).reset_index(name='Count').rename(columns={'index': 'Bank'})
    st.subheader("Top 5 Banks (Based on Count)")
    st.bar_chart(top_banks, x='Bank', y='Count')

    # Maximum to minimum per layer
    max_min_per_layer = df.groupby('Layer')['Amount'].agg(max=pd.NamedAgg(column='Amount', aggfunc='max'), min=pd.NamedAgg(column='Amount', aggfunc='min'))
    st.subheader("Maximum and Minimum Amount per Layer")
    st.dataframe(max_min_per_layer)

    # Connection to all layers (Assuming Transaction ID column exists)
    # This requires further logic to identify connections based on your data
    # Placeholder for now
    st.subheader("Connections to All Layers (Placeholder)")
    st.write("This section requires further analysis based on your specific data structure. The Transaction ID column can be used to identify connections between layers.")

    # Layer wise analysis (Assuming numeric column for analysis)
    # Modify the column name and chart type based on your data
    average_per_layer = df.groupby('Layer')['Amount'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    plt.plot(average_per_layer['Layer'], average_per_layer['Amount'])
    plt.xlabel("Layer")
    plt.ylabel("Average Amount")
    plt.title("Average Amount per Layer")
    st.pyplot()


def main():
    st