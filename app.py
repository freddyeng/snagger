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

# --- Cleanup function ---
def cleanup():
    shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)

atexit.register(cleanup)

# --- Persistent storage (keeps filenames and results) ---
stored_files = {
    "filenamesA": ["", ""],
    "filenamesB": ["", ""],
    "resultsA": [None, None],
    "resultsB": [None, None]
}

def process_file(file_path):
    """Read a file path, extract text, and run ai_request."""
    if not file_path:
        return None
    text = pdf_to_text(file_path)
    return ai_request(text)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect uploaded files
        filesA = request.files.getlist("fileA[]")
        filesB = request.files.getlist("fileB[]")

        # Save files and update persistent storage
        for i, f in enumerate(filesA):
            if f and f.filename != "":
                path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(path)
                stored_files["filenamesA"][i] = f.filename
                stored_files["resultsA"][i] = process_file(path)

        for i, f in enumerate(filesB):
            if f and f.filename != "":
                path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(path)
                stored_files["filenamesB"][i] = f.filename
                stored_files["resultsB"][i] = process_file(path)

    # Render template with stored filenames/results
    return render_template(
        "index.html",
        filenamesA=stored_files["filenamesA"],
        filenamesB=stored_files["filenamesB"],
        resultsA=stored_files["resultsA"],
        resultsB=stored_files["resultsB"]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5001)))
    app.run(debug=True, port=port)
