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
    num_pairs = 2
    user_folder = get_user_folder()

    if request.method == "POST":
        filesA = request.files.getlist("fileA[]")
        filesB = request.files.getlist("fileB[]")

        for i in range(num_pairs):
            resultA = save_and_process(filesA[i] if i < len(filesA) else None, "A", i, user_folder)
            resultB = save_and_process(filesB[i] if i < len(filesB) else None, "B", i, user_folder)

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
