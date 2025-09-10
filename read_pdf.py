import fitz  # PyMuPDF
import unicodedata
import re

def pdf_to_text(pdf_path):
    """Convert a PDF file to a cleaned single string."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    
    # --- Clean and normalize the text ---
    text = unicodedata.normalize("NFKC", text)  # normalize Unicode
    text = "".join(c for c in text if not unicodedata.category(c).startswith("C"))  # remove control chars
    text = re.sub(r"\s+", " ", text)  # collapse whitespace
    text = text.strip()  # trim leading/trailing spaces
    
    return text
