from flask import Flask, render_template, request
import os
import atexit
import shutil
from app_helpers import save_and_process, process_file, storage

UPLOAD_FOLDER = "static/uploads"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Cleanup ---
def cleanup():
    shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)

atexit.register(cleanup)

@app.route("/", methods=["GET", "POST"])
def index():
    num_pairs = 2  # adjust as needed

    if request.method == "POST":
        filesA = request.files.getlist("fileA[]")
        filesB = request.files.getlist("fileB[]")

        for i in range(num_pairs):
            resultA = save_and_process(filesA[i] if i < len(filesA) else None, "A", i, UPLOAD_FOLDER)
            resultB = save_and_process(filesB[i] if i < len(filesB) else None, "B", i, UPLOAD_FOLDER)

            storage.results[i] = {
                "fileA": resultA,
                "fileB": resultB,
                "equal": resultA == resultB
            }

    return render_template(
        "index.html",
        filenamesA=storage.filenamesA,
        filenamesB=storage.filenamesB,
        results=storage.results
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5001)))
    app.run(debug=True, port=port)
