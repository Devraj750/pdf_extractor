import streamlit as st
import PyPDF2
import pdfplumber
from PIL import Image
import io

def extract_text(pdf_file):
    """Extract text from a PDF file using PyPDF2."""
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_tables(pdf_file):
    """Extract tables from a PDF file using pdfplumber."""
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                tables.append(table)
    return tables

def extract_images(pdf_file):
    """Extract images from a PDF file."""
    images = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            for image in page.images:
                img_data = image["stream"].get_data()
                img = Image.open(io.BytesIO(img_data))
                images.append(img)
    return images

def main():
    st.title("Automated PDF Data Extractor")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file:
        st.subheader("Extracted Text")
        text = extract_text(uploaded_file)
        st.text_area("Text Content", text, height=300)
        
        st.subheader("Extracted Tables")
        tables = extract_tables(uploaded_file)
        for idx, table in enumerate(tables):
            st.write(f"Table {idx+1}")
            st.write(table)
        
        st.subheader("Extracted Images")
        images = extract_images(uploaded_file)
        for idx, img in enumerate(images):
            st.image(img, caption=f"Image {idx+1}", use_column_width=True)
    
if __name__ == "__main__":
    main()
