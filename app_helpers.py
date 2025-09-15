import os
import json
from read_pdf import pdf_to_text
from ai_request import ai_request
from flask import session
from comparisons import items_count_equal

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
    """Save uploaded file and process it with AI, storing results in session."""
    if file and file.filename != "":
        path = os.path.join(upload_folder, file.filename)
        file.save(path)

        # Store filenames in session
        filenames_key = f"filenames{side}"
        filenames = session.get(filenames_key, [""] * 2)
        filenames[index] = file.filename
        session[filenames_key] = filenames

        result = process_file(path)

        # Store results in session
        results = session.get("results", [None] * 2)
        if not results or len(results) < 2:
            results = [None] * 2
        prevA = results[index]["fileA"] if results[index] and "fileA" in results[index] else None
        prevB = results[index]["fileB"] if results[index] and "fileB" in results[index] else None
        if side == "A":
            results[index] = {
                "fileA": result,
                "fileB": prevB,
                "equal": result == prevB if prevB is not None else False,
                "items_same_size": items_count_equal(result, prevB) if prevB is not None else None,
            }
        else:
            results[index] = {
                "fileA": prevA,
                "fileB": result,
                "equal": prevA == result if prevA is not None else False,
                "items_same_size": items_count_equal(prevA, result) if prevA is not None else None,
            }
        session["results"] = results

        return result
    else:
        # Preserve previous result if no new file uploaded
        results = session.get("results", [None] * 2)
        prev = results[index] or {}
        return prev.get("fileA") if side == "A" else prev.get("fileB")
