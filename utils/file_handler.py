import pdfplumber
import json

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_text_from_json(file):
    content = json.load(file)
    return json.dumps(content, indent=2)

def extract_text_from_email(file):
    return file.read().decode("utf-8")  # assumes .txt or .eml as text
