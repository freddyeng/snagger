import os
import shutil
import logging

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO)

def get_user_folder(user_id):
    """Return the path to the user's upload folder, creating it if needed."""
    folder = os.path.join(UPLOAD_FOLDER, user_id)
    os.makedirs(folder, exist_ok=True)
    return folder

def clear_user_files(user_id):
    """Delete all files in the user's upload folder."""
    folder = get_user_folder(user_id)
    logging.info(f"Clearing files in {folder}: {os.listdir(folder)}")
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        try:
            if os.path.isfile(path):
                os.remove(path)
                logging.info(f"Deleted file: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                logging.info(f"Deleted folder: {path}")
        except Exception as e:
            logging.warning(f"Could not delete {path}: {e}")