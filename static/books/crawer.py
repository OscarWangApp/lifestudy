import os
import requests
from bs4 import BeautifulSoup

def read_list(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

def extract_info(line):
    url_part, end_index = line.rsplit("-", 1)
    start_index = url_part.rsplit("/")[-1]#.replace(".html", "").strip("0123456789")
    start_index = start_index[:start_index.index(".html")-2]
    #start_index = url_part[url_part.index(".html")-2]
    #num_part = url_part.rsplit("/")[-1].replace(".html", "").lstrip(start_index)
    num_part = url_part[url_part.index(".html")-2:url_part.index(".html")]
    start_num = int(num_part)
    end_num = int(end_index)
    base_url = url_part.replace(num_part + ".html", "")
    return base_url, start_index, start_num, end_num

def fetch_and_save(url, folder, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        p_tag = soup.find("p")
        if p_tag:
            content = p_tag.get_text(strip=True)
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Saved: {folder}/{filename}")
        else:
            print(f"No <p> tag found in {url}")
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")

def main():
    lines = read_list("lifecraw.txt")
    for line in lines:
        base_url, folder, start_num, end_num = extract_info(line)
        print(base_url, folder, start_num, end_num)
        for num in range(start_num, end_num + 1):
            index = f"{num:02d}"
            url = f"{base_url}{index}.html"
            filename = f"{folder}{index}"
            fetch_and_save(url, folder, filename)

if __name__ == "__main__":
    main()
