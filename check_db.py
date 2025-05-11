from models.database import get_db

def check_db_structure():
    db = get_db()
    cursor = db.cursor()
    
    try:
        # 檢查 auth 欄位是否存在
        cursor.execute("SHOW COLUMNS FROM user_info LIKE 'auth'")
        if not cursor.fetchone():
            # 如果不存在，則添加 auth 欄位
            cursor.execute("ALTER TABLE user_info ADD COLUMN auth VARCHAR(10) DEFAULT '1'")
            db.commit()
            print("Successfully added auth column to user_info table")
        else:
            print("Auth column already exists")
    except Exception as e:
        print(f"Error adding auth column: {e}")
        db.rollback()
    
    # 檢查 books_info 表結構
    cursor.execute("DESCRIBE books_info")
    columns = cursor.fetchall()
    print("\nBooks Info Table Structure:")
    for col in columns:
        print(col)
    
    # 檢查 user_info 表結構
    cursor.execute("DESCRIBE user_info")
    columns = cursor.fetchall()
    print("\nUser Info Table Structure:")
    for col in columns:
        print(col)
    
    # 檢查 user_books 表結構
    cursor.execute("DESCRIBE user_books")
    columns = cursor.fetchall()
    print("\nUser Books Table Structure:")
    for col in columns:
        print(col)
    
    # 檢查 books_info 表中的數據
    cursor.execute("SELECT * FROM books_info LIMIT 1")
    sample = cursor.fetchone()
    print("\nSample Books Info Data:")
    print(sample)

if __name__ == "__main__":
    check_db_structure() 