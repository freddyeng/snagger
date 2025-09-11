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

atexit.register(cleanup)  # registers the cleanup to run when app exits

def process_file(file):
    """Helper to read a file path, extract text, and run ai_request."""
    if not file:
        return None
    text = pdf_to_text(file)
    return ai_request(text)

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize results
    resultsA = [None, None]
    resultsB = [None, None]

    # Initialize filenames for display
    filenamesA = ["", ""]  # for 2 pairs
    filenamesB = ["", ""]

    if request.method == "POST":
        # Collect files from the form
        filesA = request.files.getlist("fileA[]")
        filesB = request.files.getlist("fileB[]")

        # Save files and store filenames
        for i, f in enumerate(filesA):
            if f and f.filename != "":
                path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(path)
                filenamesA[i] = f.filename
                resultsA[i] = process_file(path)

        for i, f in enumerate(filesB):
            if f and f.filename != "":
                path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(path)
                filenamesB[i] = f.filename
                resultsB[i] = process_file(path)

    return render_template(
        "index.html",
        filenamesA=filenamesA,
        filenamesB=filenamesB,
        resultsA=resultsA,
        resultsB=resultsB
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5001)))
    app.run(debug=True, port=port)
