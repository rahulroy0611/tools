import streamlit as st
import camelot
import pandas as pd
import os

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

            # Write each table to a separate sheet, removing headers and index
            for i, table in enumerate(tables):
                table.df.to_excel(writer, sheet_name=f"Table {i+1}", index=False, header=False)

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
        except Exception as e:
            st.error(f"Error converting PDF: {e}")
        finally:
            # Remove the temporary file if it exists
            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")

def main():
    st.title("PDF to Excel Converter")

    uploaded_file = st.file_uploader("Choose a PDF file")

    if uploaded_file is not None:
        pdf_file = uploaded_file.name
        st.write(f"Uploaded file: {pdf_file}")

        if st.button("Convert to Excel"):
            pdf_to_excel(uploaded_file)

if __name__ == "__main__":
    main()