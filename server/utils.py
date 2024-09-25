import fitz

def read_pdf(file_path):
    text = ""
    # Open the PDF file
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()  # Extract text from each page
    return text