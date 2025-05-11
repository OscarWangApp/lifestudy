from models.database import get_db

def create_achievement_table():
    """Create the achievement_info table if it doesn't exist."""
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Create achievement_info table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievement_info (
                code VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                `condition` TEXT NOT NULL,
                encouragement TEXT NOT NULL
            )
        """)
        db.commit()
        print("Successfully created achievement_info table")
    except Exception as e:
        print(f"Error creating achievement_info table: {e}")
        db.rollback()
        raise e

def add_achievement(code, name, condition, encouragement):
    """Add a new achievement to the achievement_info table."""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO achievement_info (code, name, `condition`, encouragement)
            VALUES (%s, %s, %s, %s)
        """, (code, name, condition, encouragement))
        db.commit()
        return True
    except Exception as e:
        print(f"Error adding achievement: {e}")
        db.rollback()
        return False

def get_all_achievements():
    """Get all achievements from the achievement_info table."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM achievement_info")
        achievements = cursor.fetchall()
        return achievements
    except Exception as e:
        print(f"Error getting achievements: {e}")
        return []

def get_achievement_by_code(code):
    """Get a specific achievement by its code."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM achievement_info WHERE code = %s", (code,))
        achievement = cursor.fetchone()
        return achievement
    except Exception as e:
        print(f"Error getting achievement: {e}")
        return None

def update_achievement(code, name, condition, encouragement):
    """Update an existing achievement."""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            UPDATE achievement_info 
            SET name = %s, `condition` = %s, encouragement = %s
            WHERE code = %s
        """, (name, condition, encouragement, code))
        db.commit()
        return True
    except Exception as e:
        print(f"Error updating achievement: {e}")
        db.rollback()
        return False

def delete_achievement(code):
    """Delete an achievement by its code."""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("DELETE FROM achievement_info WHERE code = %s", (code,))
        db.commit()
        return True
    except Exception as e:
        print(f"Error deleting achievement: {e}")
        db.rollback()
        return False 