import streamlit as st
import pandas as pd
import PyPDF2
from io import BytesIO

def extract_text_from_pdf(file):
    text = ""
    with BytesIO(file.read()) as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_data_from_text(text):
    # This is a simplified example. You might need more sophisticated parsing for complex PDF structures.
    lines = text.splitlines()
    data = []
    headers = None
    for line in lines:
        if not headers:
            headers = line.split()
            continue
        row = line.split()
        if len(row) == len(headers):
            data.append(dict(zip(headers, row)))
    return pd.DataFrame(data)

def main():
    st.title("PDF to Excel Converter")

    uploaded_file = st.file_uploader("Upload a PDF file")

    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)
        data = extract_data_from_text(text)

        st.header("Extracted Data")
        st.dataframe(data)

        # Download the data as Excel
        excel_data = BytesIO()
        data.to_excel(excel_data, index=False)
        excel_data.seek(0)
        st.download_button(
            label="Download as Excel",
            data=excel_data.getvalue(),
            file_name="extracted_data.xlsx"
        )

if __name__ == "__main__":
    main()