from flask import Flask, render_template, request, session
import os
import atexit
import shutil
import uuid
from app_helpers import save_and_process, process_file, storage

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")  # needed for sessions

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Cleanup ---
def cleanup():
    shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
atexit.register(cleanup)

@app.before_request
def assign_user():
    # Give each visitor a unique ID
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

@app.route("/", methods=["GET", "POST"])
def index():
    num_pairs = 2  # adjust as needed
    user_id = session["user_id"]
    user_folder = os.path.join(UPLOAD_FOLDER, user_id)
    os.makedirs(user_folder, exist_ok=True)

    # store results per user to avoid clashes
    if not hasattr(storage, "user_results"):
        storage.user_results = {}
    if user_id not in storage.user_results:
        storage.user_results[user_id] = {}

    if request.method == "POST":
        filesA = request.files.getlist("fileA[]")
        filesB = request.files.getlist("fileB[]")

        for i in range(num_pairs):
            resultA = save_and_process(filesA[i] if i < len(filesA) else None, "A", i, user_folder)
            resultB = save_and_process(filesB[i] if i < len(filesB) else None, "B", i, user_folder)

            storage.user_results[user_id][i] = {
                "fileA": resultA,
                "fileB": resultB,
                "equal": resultA == resultB
            }

    return render_template(
        "index.html",
        filenamesA=storage.filenamesA,
        filenamesB=storage.filenamesB,
        results=storage.user_results.get(user_id, {})
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5001)))
    app.run(debug=True, port=port)
