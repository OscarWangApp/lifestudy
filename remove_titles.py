import os
import re

def remove_titles():
    directory = "static/books/01gen"
    for filename in os.listdir(directory):
        if filename.startswith("gen"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 移除所有以"第X篇、"開頭的行
            new_content = re.sub(r'^第[一二三四五六七八九十百]+篇、.*\n', '', content, flags=re.MULTILINE)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

if __name__ == "__main__":
    remove_titles()
    print("已移除所有篇題") 