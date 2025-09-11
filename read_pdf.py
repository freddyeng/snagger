import fitz, unicodedata

def pdf_to_text(pdf_path):
    text = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text("text")
            # normalize and clean but KEEP line breaks
            page_text = unicodedata.normalize("NFKC", page_text)
            page_text = "".join(c for c in page_text if not unicodedata.category(c).startswith("C"))
            # don't collapse all whitespace — just strip ends of lines
            page_text = "\n".join(line.strip() for line in page_text.splitlines())
            text.append(page_text)
    return "\n\n".join(text)

