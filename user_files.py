import os
import shutil
from flask import session
import time

UPLOAD_FOLDER = "static/uploads"
MAX_AGE_SECONDS = 60 * 60  # 1 hour

def get_user_folder():
    """Return a unique folder for the current user."""
    user_id = session.get("user_id")
    if not user_id:
        raise RuntimeError("Session does not have user_id")
    user_folder = os.path.join(UPLOAD_FOLDER, user_id)
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def cleanup_old_folders():
    """Delete old user folders to free up space."""
    if not os.path.exists(UPLOAD_FOLDER):
        return
    now = time.time()
    for folder in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder)
        if os.path.isdir(folder_path):
            mtime = os.path.getmtime(folder_path)
            if now - mtime > MAX_AGE_SECONDS:
                shutil.rmtree(folder_path, ignore_errors=True)
