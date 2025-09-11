import json
from flask import Flask, render_template, request
import os
import atexit
import shutil
from ai_request import ai_request
from read_pdf import pdf_to_text

UPLOAD_FOLDER = "static/uploads"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Cleanup ---
def cleanup():
    shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)

atexit.register(cleanup)

# --- Persistent storage ---
num_pairs = 2  # 2×2
stored_files = {
    "filenamesA": [""] * num_pairs,
    "filenamesB": [""] * num_pairs,
    "results": [None] * num_pairs
}

# --- Helper to process AI and ensure object ---
def save_and_process(file, side, index):
    if file and file.filename != "":
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        if side == "A":
            stored_files["filenamesA"][index] = file.filename
        else:
            stored_files["filenamesB"][index] = file.filename
        return process_file(path)
    else:
        # reuse previous result if available
        prev = stored_files["results"][index] or {}
        return prev.get("fileA") if side == "A" else prev.get("fileB")

def process_file(file_path):
    """Extract text and call AI; return Python object."""
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

# --- Main route ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        filesA = request.files.getlist("fileA[]")
        filesB = request.files.getlist("fileB[]")

        for i in range(num_pairs):
            resultA = save_and_process(filesA[i] if i < len(filesA) else None, "A", i)
            resultB = save_and_process(filesB[i] if i < len(filesB) else None, "B", i)

            stored_files["results"][i] = {
                "fileA": resultA,
                "fileB": resultB,
                "equal": resultA == resultB
            }

    return render_template(
        "index.html",
        filenamesA=stored_files["filenamesA"],
        filenamesB=stored_files["filenamesB"],
        results=stored_files["results"]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5001)))
    app.run(debug=True, port=port)
