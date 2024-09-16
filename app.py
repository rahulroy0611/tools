import os
import tabula
import pandas as pd
import numpy as np
import re
import streamlit as st


def process_page(pdf_path, page, drop_columns):
    df = tabula.read_pdf(pdf_path, pages=page, multiple_tables=True)[0]
    df = pd.concat([pd.DataFrame([df.columns], columns=df.columns), df], ignore_index=True)
    df.columns = range(df.shape[1])
    df = df.drop(columns=drop_columns)
    df.columns = range(df.shape[1])
    return df


def process_pdf(file_path):
   
    df = tabula.read_pdf(file_path, pages=1, multiple_tables=True)[1]
    df = pd.concat([pd.DataFrame([df.columns], columns=df.columns), df], ignore_index=True)

    df_1 = process_page(file_path, 2, [4, 10])
    df_2 = process_page(file_path, 3, [9])
    df_3 = process_page(file_path, 4, [9])
    df_4 = process_page(file_path, 5, [9])

    data = pd.concat([df_1, df_2, df_3, df_4], axis=0)

  
    data.columns = df.iloc[0].values
    data.replace(r'^Unnamed: \d+$', np.nan, regex=True, inplace=True)

 
    def Layer(value):
        match = re.search(r'Layer : (\d+)', value)
        return int(match.group(1)) if match else None

    def Money(value):
        if pd.isna(value):
            return None
        match = re.search(r'Disputed Amount: (\d+)', str(value))
        return int(match.group(1)) if match else None

 
    data['Amount'] = data['Transaction Details'].apply(Money)
    data['Layer'] = data['Account\rNo./ (Wallet\r/PG/PA) Id\rTransaction\rId / UTR\rNumber'].apply(Layer)

    return data


st.title("PDF to Excel Converter")


uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:

    with open("temp_pdf.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF file uploaded successfully!")

    if st.button("Convert to Excel"):
        with st.spinner('Processing...'):
           
            processed_data = process_pdf("temp_pdf.pdf")


            output_excel = "converted_data.xlsx"
            processed_data.to_excel(output_excel, index=False)

            st.success("Conversion successful! Click below to download the Excel file.")
            with open(output_excel, "rb") as file:
                btn = st.download_button(
                    label="Download Excel",
                    data=file,
                    file_name="converted_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    if os.path.exists("temp_pdf.pdf"):
        os.remove("temp_pdf.pdf")