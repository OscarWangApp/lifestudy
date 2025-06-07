from models.database import get_db

class User:
    def __init__(self, id, username, password, location_id):
        self.id = id
        self.username = username
        self.password = password
        self.location_id = location_id
        
def get_locations():
    """Fetch all locations from location_info table."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM location_info")
    locations = cursor.fetchall()
    return locations

def get_user_by_account(account):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_info WHERE account = %s", (account,))
    result = cursor.fetchone()
    return result

def add_user(account, hashed_password, location, birth_year, achievement, books_info):
    """
    添加新用戶並初始化其書籍閱讀記錄
    
    Args:
        account: 用戶帳號
        hashed_password: 加密後的密碼
        location: 用戶位置
        birth_year: 出生年份
        achievement: 成就
        books_info: 書籍信息列表
    
    Returns:
        db: 數據庫連接對象（用於異常處理）
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # 開始事務
        cursor.execute("BEGIN")
        
        # 1. 插入 user_info 表
        column_names = ["account", "password", "location", "birth_year", "achievement", "auth"]
        values = [account, hashed_password, location, birth_year, achievement, "1"]  # 設置預設的 auth 值為 "1"
        
        column_str = ", ".join(column_names)
        placeholder_str = ", ".join(["%s"] * len(values))
        sql_query = f"INSERT INTO user_info ({column_str}) VALUES ({placeholder_str})"
        cursor.execute(sql_query, values)
        
        # 2. 插入 user_books 表
        # 首先插入 account 和 last_tag
        user_books_values = [account, "gen-1"]  # 添加 last_tag 默認值
        user_books_columns = ["account", "last_tag"]  # 添加 last_tag 列
        
        # 為每本書添加章節數和書籤
        for book in books_info:
            book_code = book['code'].lower()  # 轉換為小寫以匹配數據庫列名
            chapter_count = book['chapter']
            # 創建章節數字符串，用 0 填充
            chapter_str = "0" * chapter_count
            
            user_books_columns.append(book_code)
            user_books_values.append(chapter_str)
        
        # 構建 user_books 表的 SQL 語句
        user_books_column_str = ", ".join(user_books_columns)
        user_books_placeholder_str = ", ".join(["%s"] * len(user_books_values))
        user_books_sql = f"INSERT INTO user_books ({user_books_column_str}) VALUES ({user_books_placeholder_str})"
        
        # 執行 user_books 表的插入
        cursor.execute(user_books_sql, user_books_values)
        
        # 提交事務
        db.commit()
        return db
        
    except Exception as e:
        # 發生錯誤時回滾事務
        db.rollback()
        raise e

def get_user_progress(account):
    """Get user's reading progress and next achievement information."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        # Get total completed chapters
        cursor.execute("SELECT total_completed FROM user_books WHERE account = %s", (account,))
        result = cursor.fetchone()
        if not result:
            return None
        
        total_completed = result['total_completed'] or 0
        
        # Get next achievement
        cursor.execute("""
            SELECT code, name, `condition` 
            FROM achievement_info 
            WHERE CAST(SUBSTRING(`condition`, INSTR(`condition`, '=') + 1) AS UNSIGNED) > %s
            ORDER BY code ASC
            LIMIT 1
        """, (total_completed,))
        next_achievement = cursor.fetchone()
        
        return {
            'total_completed': total_completed,
            'next_achievement': next_achievement
        }
    except Exception as e:
        print(f"Error getting user progress: {e}")
        return None
    finally:
        cursor.close()
        db.close()
