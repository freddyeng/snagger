import os
import json
from read_pdf import pdf_to_text
from ai_request import ai_request
from flask import session
from comparisons import *
from formatters import *

class Storage:
    def __init__(self):
        self.filenamesA = []
        self.filenamesB = []
        self.results = []

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

        # --- Ensure session lists exist ---
        filenames_key = f"filenames{side}"
        filenames = session.get(filenames_key, [])
        results = session.get("results", [])

        # Extend lists if index is beyond current length
        while len(filenames) <= index:
            filenames.append("")
        while len(results) <= index:
            results.append(None)

        filenames[index] = file.filename
        session[filenames_key] = filenames

        result = process_file(path)

        # Get previous JSONs safely
        prevA = results[index]["fileA"] if results[index] and "fileA" in results[index] else None
        prevB = results[index]["fileB"] if results[index] and "fileB" in results[index] else None

        # Build new result dict
        if side == "A":
    # ... other code ...
            gt = largest_grand_total_key(result, prevB) if prevB is not None else None
            results[index] = {
                "fileA": result,
                "fileB": prevB,
                "items_same_size": items_count_equal(result, prevB) if prevB is not None else None,
                "largest_grand_totals": [
                    {"source": "File A", "name": gt["json1_key"], "value": gt["json1_value"]},
                    {"source": "File B", "name": gt["json2_key"], "value": gt["json2_value"]}
                ] if gt and prevB is not None else None,
                "items_detail": format_items_tables(
                    *items_comparison(result, prevB).values()
                ) if prevB is not None else None
            }
        else:
            gt = largest_grand_total_key(prevA, result) if prevA is not None else None
            results[index] = {
                "fileA": prevA,
                "fileB": result,
                "items_same_size": items_count_equal(prevA, result) if prevA is not None else None,
                "largest_grand_totals": [
                    {"source": "File A", "name": gt["json1_key"], "value": gt["json1_value"]},
                    {"source": "File B", "name": gt["json2_key"], "value": gt["json2_value"]}
                ] if gt and prevA is not None else None,
                "items_detail": format_items_tables(
                    *items_comparison(prevA, result).values()
                ) if prevA is not None else None
            }

        session["results"] = results
        return result

    else:
        # Preserve previous result if no new file uploaded
        results = session.get("results", [])
        prev = results[index] if len(results) > index and results[index] else {}
        return prev.get("fileA") if side == "A" else prev.get("fileB")
