import fitz, unicodedata
import re

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

def trim_relevant(text: str) -> str:
    keep = []
    pat_money = re.compile(r"(?:[$€£])?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?")
    keywords = (
        "Spec Number", "Description", "Quantity", "Unit Price", "Extension",
        "Unit", "U/M", "Subtotal", "Total", "Amount", "Price", "PO", "Order", "GL Code"
    )
    for line in text.splitlines():
        l = line.strip()
        if not l:
            continue
        if pat_money.search(l):
            keep.append(l)
            continue
        if any(k.lower() in l.lower() for k in keywords):
            keep.append(l)
            continue
        # short product-ish lines with mixed alnum
        if len(l) <= 120 and any(c.isdigit() for c in l) and any(c.isalpha() for c in l):
            keep.append(l)
    return "\n".join(keep)