import os

def add_titles():
    # 讀取篇題
    with open('genesis_chapters.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 解析篇題
    titles = {}
    for line in lines:
        if line.startswith('第') and ':' in line:
            parts = line.split(':')
            num = int(parts[0].split('篇')[0].split('第')[1].strip())
            title = parts[1].strip()
            titles[num] = title
    
    # 處理每個文件
    directory = "static/books/01gen"
    for filename in os.listdir(directory):
        if filename.startswith("gen"):
            # 從文件名獲取章節號
            chapter_num = int(filename[3:])
            
            # 找到對應的篇題
            if chapter_num in titles:
                title = titles[chapter_num]
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 在文件開頭添加篇題
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(title + '\n\n' + content)

if __name__ == "__main__":
    add_titles()
    print("已添加篇題到所有文件") 