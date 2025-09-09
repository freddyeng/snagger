from flask import Flask, render_template, request
import os
from compare_utils import filenames_match

UPLOAD_FOLDER = "static/uploads"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    file1 = request.form.get("file1")
    file2 = request.form.get("file2")
    if file1 and file2:
        result = filenames_match(file1, file2)

    return render_template("index.html", files=files, result=result, file1=file1, file2=file2)

if __name__ == "__main__":
    # Prefer PORT or FLASK_RUN_PORT env vars; default to 5001 to avoid macOS AirPlay conflict on 5000
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5001)))
    app.run(debug=True, port=port)
