import fitz
import logging

def read_pdf(file_path):
    text = ""
    # Open the PDF file
    logging.info(f"Opening PDF file: {file_path}")
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()  # Extract text from each page
    return text