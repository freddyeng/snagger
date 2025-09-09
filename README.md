# File Comparison Web App (PDF MVP)

Compare uploaded PDF files with local PDFs and see matches by filename. All functionality is on a single page for the MVP.

---

## Requirements

- Python 3.11+
- Virtual environment (recommended)
- Dependencies listed in `requirements.txt`

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd snagger   # change to your repo folder name
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> Your terminal prompt should now show `(.venv)`.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Make sure `requirements.txt` includes `Flask` and `python-dotenv`. Optional: `pandas`, `PyMuPDF` for future features.

### 4. Run the Flask app with auto-reload

Option A (recommended, uses `.flaskenv`):

```bash
flask run
```

Option B (if `.flaskenv` isn’t being loaded):

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
FLASK_RUN_PORT=5001 flask run
```

- Open a browser and go to: [http://127.0.0.1:5001](http://127.0.0.1:5001)  
- The server auto-reloads when Python code changes.

---

## Usage

1. **Upload files** using the upload form.  
2. **See all uploaded files** in a table.  
3. **Select two files** to compare (radio buttons).  
4. **Click Compare** — result currently only checks if filenames match.  

---

## Project Structure

```
snagger/
│
├── .venv/                 # Virtual environment (ignored in repo)
├── .flaskenv              # Flask CLI defaults (port 5001)
├── app.py                 # Flask backend
├── compare_utils.py       # File comparison logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Single-page UI
├── static/
│   ├── uploads/           # Uploaded files stored here
│   └── css/               # Optional stylesheets
└── README.md              # This file
```

---

## Notes

- MVP feature: comparison is **just filename match**.  
- Everything runs on a single page for simplicity.  
- You can expand `compare_utils.py` later for **content-based PDF comparison**.  
- All Flask Python code changes auto-reload when `FLASK_ENV=development` is set.  
- Keep `.venv` ignored in your git repo (`.gitignore`) to avoid committing virtual environment files.  
- Default dev port is 5001 (to avoid macOS AirPlay using 5000). If you prefer 5000, disable AirPlay Receiver or run `flask run --port 5000`.  
