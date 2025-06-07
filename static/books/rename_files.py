import os
import re

def rename_files_in_directory(directory):
    # Get all files in the directory
    files = os.listdir(directory)
    
    for filename in files:
        # Skip if it's a directory
        if os.path.isdir(os.path.join(directory, filename)):
            continue
            
        # Try to extract number from filename with letters
        match = re.search(r'[a-zA-Z]+(\d+)', filename)
        if match:
            number = match.group(1)
        else:
            # If no letters found, try to match just the number
            match = re.search(r'^(\d+)$', filename)
            if match:
                number = match.group(1)
            else:
                continue
                
        # Create new filename with three digits by padding with leading zeros
        new_filename = f"{int(number):03d}"
        
        # Create full paths
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        
        # Only rename if the new name is different
        if old_path != new_path:
            os.rename(old_path, new_path)
            print(f"Renamed {filename} to {new_filename}")

def main():
    # Get the current directory (where the script is located)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Process each subdirectory
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            print(f"\nProcessing directory: {item}")
            rename_files_in_directory(item_path)

if __name__ == "__main__":
    main() 