import requests
from bs4 import BeautifulSoup
import re
import time

def scrape_genesis_chapters():
    """
    爬取創世記生命讀經的篇題
    返回一個字典，鍵為章節號，值為篇題
    """
    url = "https://www.lsmchinese.org/lifestudy/ot/gen-idx.html"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }
    
    try:
        print(f"正在訪問 URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"請求失敗，狀態碼: {response.status_code}")
            return {}
        
        print(f"請求成功，狀態碼: {response.status_code}")
        print(f"響應內容長度: {len(response.text)} 字節")
        
        with open('response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("已保存響應內容到 response.html")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有可能的鏈接
        all_links = soup.find_all('a')
        print(f"找到 {len(all_links)} 個鏈接")
        
        chapters = {}
        processed_chapters = set()
        
        # 首先處理標準格式的鏈接（gen001.html - gen120.html）
        for link in all_links:
            href = link.get('href', '')
            chapter_match = re.search(r'gen(\d{3})\.html', href)
            if chapter_match:
                chapter_num = str(int(chapter_match.group(1)))
                if chapter_num not in processed_chapters:
                    title = link.text.strip()
                    if "第" in title and "篇" in title:
                        chapters[chapter_num] = title
                        processed_chapters.add(chapter_num)
                        print(f"找到章節 {chapter_num}: {title}")
        
        # 檢查是否有缺失的章節
        missing_chapters = []
        for i in range(1, 121):  # 假設總共有120篇
            if str(i) not in chapters:
                missing_chapters.append(i)
        
        if missing_chapters:
            print("\n缺失的章節:")
            for chapter in missing_chapters:
                print(f"第 {chapter} 篇")
        
        return chapters
    
    except requests.exceptions.RequestException as e:
        print(f"請求異常: {e}")
        return {}
    except Exception as e:
        print(f"爬取過程中發生錯誤: {e}")
        return {}

def save_to_file(chapters, filename="genesis_chapters.txt"):
    """
    將爬取到的篇題保存到文件中
    """
    try:
        with open(filename, 'w', encoding='utf-8-sig') as f:
            f.write("創世記生命讀經篇題\n")
            f.write("=" * 20 + "\n\n")
            
            # 按章節號排序
            for chapter_num in sorted(chapters.keys(), key=int):
                f.write(f"第 {chapter_num} 篇: {chapters[chapter_num]}\n")
            
            # 添加統計信息
            f.write(f"\n總計: {len(chapters)} 篇")
            
            # 如果有缺失的章節，也記錄下來
            missing = [str(i) for i in range(1, 121) if str(i) not in chapters]
            if missing:
                f.write("\n\n缺失的章節: " + ", ".join(missing))
        
        print(f"篇題已保存到 {filename}")
    
    except Exception as e:
        print(f"保存文件時發生錯誤: {e}")

def main():
    print("開始爬取創世記生命讀經篇題...")
    chapters = scrape_genesis_chapters()
    
    if chapters:
        print(f"成功爬取到 {len(chapters)} 個篇題")
        save_to_file(chapters)
    else:
        print("未能爬取到任何篇題")

if __name__ == "__main__":
    main() 