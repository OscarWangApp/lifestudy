import os
import re
from models.database import get_db
from flask import current_app

def get_book_content(book_sql, book_code, chapter):
    """
    從static/books目錄讀取指定書籍和章節的內容
    
    Args:
        book_sql: 書籍的sql值（用於目錄名）
        book_code: 書籍的代碼
        chapter: 章節號（會自動補零）
    
    Returns:
        檔案內容的字符串，如果檔案不存在則返回None
    """
    try:
        # 格式化sql值（補零為兩位數）
        formatted_sql = str(book_sql).zfill(2)
        
        # 統一所有章節號都用三碼格式
        formatted_chapter = str(chapter).zfill(3)
        
        # 構建檔案路徑
        folder_name = f"{formatted_sql}{book_code.lower()}"
        file_path = os.path.join(current_app.root_path, 'static', 'books', folder_name, formatted_chapter)
        
        # 檢查檔案是否存在
        if not os.path.exists(file_path):
            return None
        
        # 讀取檔案內容
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # 處理連續空行：將連續三行或以上沒有實際文字的行縮減為一行
        result_lines = []
        empty_line_count = 0
        
        for line in lines:
            # 檢查行是否只包含空白字符
            if not line.strip():
                empty_line_count += 1
                # 如果連續空行數小於3，保留這些空行
                if empty_line_count < 3:
                    result_lines.append(line)
                # 如果連續空行數達到3，只保留一個空行
                elif empty_line_count == 3:
                    # 移除之前添加的空行，只保留一個
                    result_lines = result_lines[:-2]
                    result_lines.append(line)
                # 如果連續空行數大於3，忽略這些空行
            else:
                # 遇到非空行，重置計數器
                empty_line_count = 0
                result_lines.append(line)
        
        # 將處理後的行合併為字符串
        content = ''.join(result_lines)
        return content
    except Exception as e:
        return None 