import fitz
import logging

import os


def read_pdf(file_path):
    text = ""
    # Open the PDF file
    logging.info(f"Opening PDF file: {file_path}")
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()  # Extract text from each page
    return text


def get_assets_file_path(file_name):

    # Get the directory of the current script
    currDir = os.path.dirname(__file__)

    # Define the path to the 'ar-law.pdf' file in the 'assets' directory
    filePath = os.path.join(currDir, f'../assets/{file_name}')

    # Normalize the path (optional)
    filePath = os.path.normpath(filePath)

    return filePath
