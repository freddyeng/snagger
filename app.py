from flask import Flask, render_template, request, session
import os
import atexit
import uuid
from app_helpers import save_and_process, storage
from user_files import get_user_folder, cleanup_old_folders

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")

# --- Cleanup on exit ---
atexit.register(cleanup_old_folders)

@app.before_request
def assign_user():
    # Assign a unique ID to each session
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    cleanup_old_folders()  # optional: clean old folders on each request

@app.route("/", methods=["GET", "POST"])
def index():
    user_folder = get_user_folder()

    # Ensure session lists exist; start with 1 empty row
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
            save_and_process(filesA[i] if i < len(filesA) else None, "A", i, user_folder)
            save_and_process(filesB[i] if i < len(filesB) else None, "B", i, user_folder)

    return render_template(
        "index.html",
        filenamesA=filenamesA,
        filenamesB=filenamesB,
        results=results
    )

@app.route("/clear_all_data", methods=["POST"])
def clear_all_data():
    user_folder = get_user_folder()
    session.clear()
    # Remove the user's upload folder and its contents
    import shutil
    import os
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
    return ("", 204)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5001)))
    app.run(debug=True, port=port)
