import os
import shutil
import logging

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO)

def clear_all_files():
    """Delete all files in the uploads folder."""
    logging.info(f"Clearing files in {UPLOAD_FOLDER}: {os.listdir(UPLOAD_FOLDER)}")
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(path):
                os.remove(path)
                logging.info(f"Deleted file: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                logging.info(f"Deleted folder: {path}")
        except Exception as e:
            logging.warning(f"Could not delete {path}: {e}")
