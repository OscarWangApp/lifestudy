import requests
from bs4 import BeautifulSoup
import re
import json
import time
import os

def get_book_info(book_num):
    url = f"https://line.twgbr.org/life-study/{book_num}.html"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the script tag containing the bible object
        for script in soup.find_all('script'):
            if script.string and 'var bible' in script.string:
                # Extract the object content
                match = re.search(r'var\s+bible\s*=\s*({[^}]+})', script.string)
                if match:
                    js_obj = match.group(1)
                    # Convert JavaScript object to valid JSON
                    js_obj = js_obj.replace("'", '"')  # Replace single quotes with double quotes
                    js_obj = re.sub(r'(\w+):', r'"\1":', js_obj)  # Add quotes to property names
                    js_obj = re.sub(r',\s*}', '}', js_obj)  # Remove trailing comma before closing brace
                    return json.loads(js_obj)
                    
        print(f"Book {book_num:02d}: Could not find book info")
        return None
    except Exception as e:
        print(f"Book {book_num:02d}: Error - {str(e)}")
        return None

def download_audio_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the file
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def scan_all_books():
    print("Downloading audio files for all books:")
    print("-" * 60)
    
    for book_num in range(1, 67):  # 1 to 66
        book_info = get_book_info(book_num)
        if not book_info:
            continue
            
        ot_nt = book_info.get('ot_nt', '')
        book_mp4_prefix = book_info.get('bookMP4Prefix', '')
        num_chapters = book_info.get('numChapters', 0)
        
        print(f"\nBook {book_num:02d}:")
        print(f"ot_nt: {ot_nt}")
        print(f"bookMP4Prefix: {book_mp4_prefix}")
        print(f"numChapters: {num_chapters}")
        
        # Create directory for this book
        book_dir = f"static/audio/{book_num:02d}{book_mp4_prefix}"
        
        # Download each chapter's audio file
        for chapter in range(1, num_chapters + 1):
            chapter_num = f"{chapter:03d}"
            audio_url = f"https://line.twgbr.org/life-study/mp3/{ot_nt}/{book_mp4_prefix}-{chapter_num}.mp3"
            save_path = f"{book_dir}/{chapter_num}.mp3"
            
            print(f"Chapter {chapter_num}: Downloading...")
            if download_audio_file(audio_url, save_path):
                print(f"Saved to: {save_path}")
            else:
                print(f"Failed to download: {audio_url}")
            
        # Add a small delay to be nice to the server
        time.sleep(1)

if __name__ == "__main__":
    scan_all_books() 