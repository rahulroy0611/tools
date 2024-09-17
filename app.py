import streamlit as st
import camelot

def pdf_to_excel(pdf_file):
    """Converts a PDF file to Excel.

    Args:
        pdf_file (str): Path to the PDF file.
    """

    try:
        tables = camelot.read_pdf(pdf_file, flavor='lattice')
        excel_file = pdf_file.replace(".pdf", ".xlsx")

        # Create an Excel writer
        writer = pd.ExcelWriter(excel_file, engine='openpyxl')

        # Write each table to a separate sheet
        for i, table in enumerate(tables):
            table.df.to_excel(writer, sheet_name=f"Table {i+1}")

        writer.save()
        st.success(f"PDF converted to Excel: {excel_file}")

    except Exception as e:
        st.error(f"Error converting PDF: {e}")

def main():
    st.title("PDF to Excel Converter")

    uploaded_file = st.file_uploader("Choose a PDF file")

    if uploaded_file is not None:
        pdf_file = uploaded_file.name
        st.write(f"Uploaded file: {pdf_file}")

        if st.button("Convert to Excel"):
            pdf_to_excel(pdf_file)

if __name__ == "__main__":
    main()