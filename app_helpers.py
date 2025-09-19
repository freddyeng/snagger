import os
import json
from read_pdf import pdf_to_text
from ai_request import ai_request
from flask import session
from comparisons import largest_grand_total_key, items_comparison
from formatters import format_items_tables

def process_file(file_path):
    """Extract text from PDF, call AI, and parse JSON if possible."""
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
    """Save uploaded file, process it, and update session results."""
    filenames_key = f"filenames{side}"
    filenames = session.get(filenames_key, [])
    results = session.get("results", [])

    # Extend session lists if needed
    while len(filenames) <= index:
        filenames.append("")
    while len(results) <= index:
        results.append(None)

    # Ensure current slot is a dict
    if results[index] is None:
        results[index] = {}

    if file and file.filename:
        path = os.path.join(upload_folder, file.filename)
        file.save(path)

        # Process the file
        result_json = process_file(path)
        results[index][f"file{side}"] = result_json
        filenames[index] = file.filename
        session[filenames_key] = filenames

        # Compute largest grand total
        gt = largest_grand_total_key(result_json)
        results[index][f"largest_grand_total_{side}"] = gt

        # Compute item table
        df_items = items_comparison(result_json)
        results[index][f"items_table_{side}"] = format_items_tables(df_items)

        # Save updated results back to session
        session["results"] = results

        return result_json
    else:
        # Return existing JSON if no new file uploaded
        return results[index].get(f"file{side}")
