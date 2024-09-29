import fitz
import logging

import os


def read_pdf(file_path):
    """Read text from a PDF file"""
    text = ""
    # Open the PDF file
    logging.info(f"Opening PDF file: {file_path}")
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()  # Extract text from each page
    return text


def get_assets_file_path(file_name):
    """Get the path to a file in the 'assets' directory"""
    currDir = os.path.dirname(__file__)

    # Define the path to the assests directory
    filePath = os.path.join(currDir, f'../assets/{file_name}')
    # Normalize path
    filePath = os.path.normpath(filePath)

    return filePath
