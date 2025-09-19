import os
import json
from read_pdf import pdf_to_text
from ai_request import ai_request, ai_request_totals
from flask import session
from comparisons import largest_grand_total_key, items_comparison
from formatters import format_items_tables
from read_pdf import trim_relevant

def process_file(file_path):
    """Extract text from PDF, call AI, and parse JSON if possible."""
    if not file_path:
        return None
    full_text = pdf_to_text(file_path)
    text = trim_relevant(full_text)

    raw_result = ai_request(text)
    if isinstance(raw_result, str):
        try:
            data = json.loads(raw_result)
        except json.JSONDecodeError:
            return raw_result
    else:
        data = raw_result

    # Compute sum of item totals
    try:
        items = data.get("items", []) or []
        computed = sum(
            float(i.get("total_price")) for i in items
            if i is not None and i.get("total_price") is not None
        )
    except Exception:
        computed = 0.0

    # Ensure grand_totals exists
    gt = data.get("grand_totals") or {}
    data["grand_totals"] = gt

    # If totals missing, fetch totals-only pass
    if not gt:
        try:
            totals_only = ai_request_totals(text)
            if isinstance(totals_only, str):
                totals_obj = json.loads(totals_only)
            else:
                totals_obj = totals_only
            data["grand_totals"] = totals_obj.get("grand_totals", {}) or {}
            gt = data["grand_totals"]
        except Exception:
            pass

    # Cross-validate: prefer Computed Total if model total is missing or off by >5%
    try:
        model_total = None
        for k, v in gt.items():
            if "total" in k.lower() and isinstance(v, (int, float)):
                model_total = v
                break
        if computed > 0 and (model_total is None or abs(model_total - computed) / computed > 0.05):
            gt["Computed Total"] = round(computed, 2)
            data["grand_totals"] = gt
    except Exception:
        pass

    return data

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
