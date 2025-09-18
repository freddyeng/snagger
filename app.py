from flask import Flask, render_template, request, session, current_app
import os
import shutil
from app_helpers import save_and_process  # your existing save/process logic

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")

UPLOAD_FOLDER = "static/uploads"

def get_upload_folder():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    return UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    folder = get_upload_folder()

    # initialize session keys
    if "filenamesA" not in session:
        session["filenamesA"] = [""]
    if "filenamesB" not in session:
        session["filenamesB"] = [""]
    if "results" not in session:
        session["results"] = [None]

    filenamesA = session["filenamesA"]
    filenamesB = session["filenamesB"]
    results = session["results"]

    if request.method == "POST":
        filesA = request.files.getlist("fileA[]")
        filesB = request.files.getlist("fileB[]")
        num_rows = max(len(filesA), len(filesB), len(filenamesA))

        for i in range(num_rows):
            save_and_process(filesA[i] if i < len(filesA) else None, "A", i, folder)
            save_and_process(filesB[i] if i < len(filesB) else None, "B", i, folder)

    return render_template(
        "index.html",
        filenamesA=filenamesA,
        filenamesB=filenamesB,
        results=results
    )

@app.route("/clear_all_data", methods=["POST"])
def clear_all_data():
    folder = get_upload_folder()
    current_app.logger.info(f"Clearing files in {folder}: {os.listdir(folder)}")

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                current_app.logger.info(f"Deleted file: {file_path}")
        except Exception as e:
            current_app.logger.error(f"Failed to delete {file_path}: {e}")

    # Reset session
    session.clear()
    session["filenamesA"] = [""]
    session["filenamesB"] = [""]
    session["results"] = [None]

    current_app.logger.info("Session cleared (except keys).")
    return ("", 204)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
