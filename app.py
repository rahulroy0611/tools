import os
import tabula
import pandas as pd
import numpy as np
import re
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns


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

        # Remove non-numeric characters and leading/trailing spaces
        value = re.sub(r'[^\d]', '', str(value)).strip()

        # Check if the value is empty after cleaning
        if not value:
            return None

        try:
            return int(value)
        except ValueError:
            # Handle cases where the value still cannot be converted to int
            # You might want to log this or return a default value
            return None

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

            # Existing Charts
            st.subheader("Distribution of Disputed Amounts")
            fig, ax = plt.subplots()
            ax.hist(processed_data['Amount'], bins='auto')
            ax.set_xlabel('Disputed Amount')
            ax.set_ylabel('Frequency')
            st.pyplot(fig)

            st.subheader("Average Disputed Amount by Layer")
            avg_amount_per_layer = processed_data.groupby('Layer')['Amount'].mean()
            st.bar_chart(avg_amount_per_layer)

            # New Charts
            # Time-based Analysis (assuming a 'Date' column)
            if 'Date' in processed_data.columns:
                st.subheader("Disputed Amounts Over Time")
                fig, ax = plt.subplots()
                ax.plot(processed_data['Date'], processed_data['Amount'])
                ax.set_xlabel('Date')
                ax.set_ylabel('Disputed Amount')
                st.pyplot(fig)

            # Transaction Details Analysis (assuming 'Transaction Details' contains textual data)
            st.subheader("Word Cloud of Transaction Details")
            word_cloud = WordCloud(width=800, height=400).generate(' '.join(processed_data['Transaction Details'].astype(str)))
            fig, ax = plt.subplots()
            ax.imshow(word_cloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

            # Account-based Analysis (assuming 'Account\rNo./ (Wallet\r/PG/PA) Id\rTransaction\rId / UTR\rNumber' is the account column)
            st.subheader("Top Disputed Accounts")
            top_accounts = processed_data.groupby('Account\rNo./ (Wallet\r/PG/PA) Id\rTransaction\rId / UTR\rNumber')['Amount'].sum().sort_values(ascending=False)
            st.bar_chart(top_accounts[:10])  # Display top 10 accounts

            # Correlation Analysis (if applicable)
            if processed_data.select_dtypes(include='number').shape[1] > 1:
                st.subheader("Correlation Matrix")
                correlation_matrix = processed_data.corr()
                st.dataframe(correlation_matrix)

            # Interactive Filters
            st.subheader("Interactive Filters")
            disputed_amount_filter = st.slider("Filter Disputed Amount:", min_value=processed_data['Amount'].dropna().min(), max_value=processed_data['Amount'].dropna().max())

            # Filter data based on the slider, handling None values
            if disputed_amount_filter is not None:
                filtered_data = processed_data[processed_data['Amount'].fillna(0) >= disputed_amount_filter]
            else:
                filtered_data = processed_data  # Handle case where slider value is None

            st.write(filtered_data)  # Or display other charts or visualizations based on filtered data

    if os.path.exists("temp_pdf.pdf"):
        os.remove("temp_pdf.pdf")