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


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    files = os.listdir(app.config["UPLOAD_FOLDER"])

    # Handle file upload
    if request.method == "POST" and "file" in request.files:
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename))
        files = os.listdir(app.config["UPLOAD_FOLDER"])

    # Handle comparison
    file1_name = request.form.get("file1")
    # file2_name = request.form.get("file2")

    # if file1_name and file2_name:
    if file1_name:
        file1_path = os.path.join(app.config["UPLOAD_FOLDER"], file1_name)
        # file2_path = os.path.join(app.config["UPLOAD_FOLDER"], file2_name)

        text1 = pdf_to_text(file1_path)
        # text2 = pdf_to_text(file2_path)

        # if text1 == text2:
        #     result = "Exact match"
        # else:
        #     result = ai_request(text1, text2)
        result = ai_request(text1)

    return render_template("index.html", files=files, result=result)

if __name__ == "__main__":
    # Prefer PORT or FLASK_RUN_PORT env vars; default to 5001 to avoid macOS AirPlay conflict on 5000
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5001)))
    app.run(debug=True, port=port)
