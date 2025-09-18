from flask import Flask, render_template, request, session
import os
import uuid
from user_files import get_user_folder, clear_user_files
from app_helpers import save_and_process

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")

@app.before_request
def assign_user_id():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

@app.route("/", methods=["GET", "POST"])
def index():
    user_folder = get_user_folder(session["user_id"])

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
    user_id = session.get("user_id")
    if user_id:
        clear_user_files(user_id)
    session.clear()
    # Re-assign user_id so the user keeps their folder for the next session
    session["user_id"] = user_id if user_id else str(uuid.uuid4())
    session["filenamesA"] = [""]
    session["filenamesB"] = [""]
    session["results"] = [None]
    return ("", 204)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)