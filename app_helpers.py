import os
import json
from read_pdf import pdf_to_text
from ai_request import ai_request

class Storage:
    """Persistent storage for uploaded filenames and AI results."""
    def __init__(self, num_pairs=2):
        self.filenamesA = [""] * num_pairs
        self.filenamesB = [""] * num_pairs
        self.results = [None] * num_pairs  # list of dicts {"fileA":..., "fileB":..., "equal":...}

storage = Storage()

# --- Helper functions ---
def process_file(file_path):
    """Extract text from PDF and call AI; parse JSON if possible."""
    if not file_path:
        return None
    text = pdf_to_text(file_path)
    raw_result = ai_request(text)
    if isinstance(raw_result, str):
        try:
            return json.loads(raw_result)
        except json.JSONDecodeError:
            return raw_result
    return raw_result

def save_and_process(file, side, index, upload_folder):
    """Save uploaded file and process it with AI."""
    if file and file.filename != "":
        path = os.path.join(upload_folder, file.filename)
        file.save(path)

        if side == "A":
            storage.filenamesA[index] = file.filename
        else:
            storage.filenamesB[index] = file.filename

        return process_file(path)
    else:
        # Preserve previous result if no new file uploaded
        prev = storage.results[index] or {}
        return prev.get("fileA") if side == "A" else prev.get("fileB")
