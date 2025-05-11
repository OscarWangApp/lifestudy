import mysql.connector

def get_db():
    """Establish and return a database connection."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="lifestudy"
    )
    return db

def init_db():
    """Initialize the database by creating necessary tables if they don't exist."""
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Create user_info table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_info (
                account VARCHAR(50) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                location VARCHAR(100) DEFAULT NULL,
                birth_year VARCHAR(4) DEFAULT NULL,
                achievement VARCHAR(50) DEFAULT NULL,
                auth VARCHAR(10) DEFAULT '1'
            )
        """)
        
        # Create user_books table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_books (
                account VARCHAR(50) PRIMARY KEY,
                gen VARCHAR(100) DEFAULT '0' * 50,
                exo VARCHAR(100) DEFAULT '0' * 40,
                lev VARCHAR(100) DEFAULT '0' * 27,
                num VARCHAR(100) DEFAULT '0' * 36,
                deu VARCHAR(100) DEFAULT '0' * 34,
                jos VARCHAR(100) DEFAULT '0' * 24,
                jdg VARCHAR(100) DEFAULT '0' * 21,
                rut VARCHAR(100) DEFAULT '0' * 4,
                sam VARCHAR(100) DEFAULT '0' * 31,
                kg1 VARCHAR(100) DEFAULT '0' * 22,
                kg2 VARCHAR(100) DEFAULT '0' * 25,
                ch1 VARCHAR(100) DEFAULT '0' * 29,
                ch2 VARCHAR(100) DEFAULT '0' * 36,
                ezr VARCHAR(100) DEFAULT '0' * 10,
                neh VARCHAR(100) DEFAULT '0' * 13,
                est VARCHAR(100) DEFAULT '0' * 10,
                job VARCHAR(100) DEFAULT '0' * 42,
                psa VARCHAR(100) DEFAULT '0' * 150,
                pro VARCHAR(100) DEFAULT '0' * 31,
                ecc VARCHAR(100) DEFAULT '0' * 12,
                sng VARCHAR(100) DEFAULT '0' * 8,
                isa VARCHAR(100) DEFAULT '0' * 66,
                jer VARCHAR(100) DEFAULT '0' * 52,
                lam VARCHAR(100) DEFAULT '0' * 5,
                ezk VARCHAR(100) DEFAULT '0' * 48,
                dan VARCHAR(100) DEFAULT '0' * 12,
                hos VARCHAR(100) DEFAULT '0' * 14,
                jol VARCHAR(100) DEFAULT '0' * 3,
                amo VARCHAR(100) DEFAULT '0' * 9,
                oba VARCHAR(100) DEFAULT '0' * 1,
                jon VARCHAR(100) DEFAULT '0' * 4,
                mic VARCHAR(100) DEFAULT '0' * 7,
                nam VARCHAR(100) DEFAULT '0' * 3,
                hab VARCHAR(100) DEFAULT '0' * 3,
                zep VARCHAR(100) DEFAULT '0' * 3,
                hag VARCHAR(100) DEFAULT '0' * 2,
                zec VARCHAR(100) DEFAULT '0' * 14,
                mal VARCHAR(100) DEFAULT '0' * 4,
                mat VARCHAR(100) DEFAULT '0' * 28,
                mrk VARCHAR(100) DEFAULT '0' * 16,
                luke VARCHAR(100) DEFAULT '0' * 24,
                john VARCHAR(100) DEFAULT '0' * 21,
                act VARCHAR(100) DEFAULT '0' * 28,
                rom VARCHAR(100) DEFAULT '0' * 16,
                co1 VARCHAR(100) DEFAULT '0' * 16,
                co2 VARCHAR(100) DEFAULT '0' * 13,
                gal VARCHAR(100) DEFAULT '0' * 6,
                eph VARCHAR(100) DEFAULT '0' * 6,
                phi VARCHAR(100) DEFAULT '0' * 4,
                col VARCHAR(100) DEFAULT '0' * 4,
                th1 VARCHAR(100) DEFAULT '0' * 5,
                th2 VARCHAR(100) DEFAULT '0' * 4,
                ti1 VARCHAR(100) DEFAULT '0' * 6,
                ti2 VARCHAR(100) DEFAULT '0' * 4,
                tit VARCHAR(100) DEFAULT '0' * 3,
                phm VARCHAR(100) DEFAULT '0' * 1,
                heb VARCHAR(100) DEFAULT '0' * 13,
                jam VARCHAR(100) DEFAULT '0' * 5,
                pet1 VARCHAR(100) DEFAULT '0' * 5,
                pet2 VARCHAR(100) DEFAULT '0' * 3,
                jo1 VARCHAR(100) DEFAULT '0' * 5,
                jo2 VARCHAR(100) DEFAULT '0' * 1,
                jo3 VARCHAR(100) DEFAULT '0' * 1,
                jud VARCHAR(100) DEFAULT '0' * 1,
                rev VARCHAR(100) DEFAULT '0' * 22,
                last_tag VARCHAR(50) DEFAULT NULL,
                total_completed INT DEFAULT 0,
                FOREIGN KEY (account) REFERENCES user_info(account)
            )
        """)
        
        # Create achievement_info table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievement_info (
                code VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                `condition` TEXT NOT NULL,
                encouragement TEXT NOT NULL
            )
        """)
        
        db.commit()
        print("Successfully initialized database tables")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

def init_achievement_info():
    """Initialize achievement information in the database."""
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Start transaction
        cursor.execute("BEGIN")
        
        # Clear existing achievements
        cursor.execute("DELETE FROM achievement_info")
        
        # Add achievements
        achievements = [
            ("00001", "第一章", "Σ(chapters_completed) = 1", "恭喜你完成第一章！這是你的第一個里程碑。"),
            ("00005", "五章", "Σ(chapters_completed) = 5", "太棒了！你已經完成了五章。繼續保持！"),
            ("00010", "十章", "Σ(chapters_completed) = 10", "十章的成就達成！你的堅持令人印象深刻。"),
            ("00050", "五十章", "Σ(chapters_completed) = 50", "五十章！你已經完成了相當可觀的閱讀量。"),
            ("00100", "百章", "Σ(chapters_completed) = 100", "百章成就！你的 dedication 令人敬佩。"),
            ("00150", "一百五十章", "Σ(chapters_completed) = 150", "一百五十章！你正在穩步前進。"),
            ("00200", "兩百章", "Σ(chapters_completed) = 200", "兩百章！你已經完成了聖經的很大一部分。"),
            ("00250", "兩百五十章", "Σ(chapters_completed) = 250", "兩百五十章！你的進步令人驚嘆。"),
            ("00300", "三百章", "Σ(chapters_completed) = 300", "三百章！你已經完成了聖經的三分之一。"),
            ("00350", "三百五十章", "Σ(chapters_completed) = 350", "三百五十章！你的堅持令人感動。"),
            ("00400", "四百章", "Σ(chapters_completed) = 400", "四百章！你已經完成了聖經的很大一部分。"),
            ("00450", "四百五十章", "Σ(chapters_completed) = 450", "四百五十章！你的進步令人印象深刻。"),
            ("00500", "五百章", "Σ(chapters_completed) = 500", "五百章！你已經完成了聖經的一半以上。"),
            ("00550", "五百五十章", "Σ(chapters_completed) = 550", "五百五十章！你的 dedication 令人敬佩。"),
            ("00600", "六百章", "Σ(chapters_completed) = 600", "六百章！你正在穩步前進。"),
            ("00650", "六百五十章", "Σ(chapters_completed) = 650", "六百五十章！你的進步令人驚嘆。"),
            ("00700", "七百章", "Σ(chapters_completed) = 700", "七百章！你已經完成了聖經的三分之二。"),
            ("00750", "七百五十章", "Σ(chapters_completed) = 750", "七百五十章！你的堅持令人感動。"),
            ("00800", "八百章", "Σ(chapters_completed) = 800", "八百章！你已經完成了聖經的很大一部分。"),
            ("00850", "八百五十章", "Σ(chapters_completed) = 850", "八百五十章！你的進步令人印象深刻。"),
            ("00900", "九百章", "Σ(chapters_completed) = 900", "九百章！你已經完成了聖經的很大一部分。"),
            ("00950", "九百五十章", "Σ(chapters_completed) = 950", "九百五十章！你的 dedication 令人敬佩。"),
            ("01000", "千章", "Σ(chapters_completed) = 1000", "千章成就！你已經完成了聖經的一半以上。"),
            ("01050", "一千零五十章", "Σ(chapters_completed) = 1050", "一千零五十章！你的進步令人驚嘆。"),
            ("01100", "一千一百章", "Σ(chapters_completed) = 1100", "一千一百章！你正在穩步前進。"),
            ("01150", "一千一百五十章", "Σ(chapters_completed) = 1150", "一千一百五十章！你的堅持令人感動。"),
            ("01200", "一千二百章", "Σ(chapters_completed) = 1200", "一千二百章！你已經完成了聖經的很大一部分。"),
            ("01250", "一千二百五十章", "Σ(chapters_completed) = 1250", "一千二百五十章！你的進步令人印象深刻。"),
            ("01300", "一千三百章", "Σ(chapters_completed) = 1300", "一千三百章！你已經完成了聖經的三分之二以上。"),
            ("01350", "一千三百五十章", "Σ(chapters_completed) = 1350", "一千三百五十章！你的 dedication 令人敬佩。"),
            ("01400", "一千四百章", "Σ(chapters_completed) = 1400", "一千四百章！你正在穩步前進。"),
            ("01450", "一千四百五十章", "Σ(chapters_completed) = 1450", "一千四百五十章！你的進步令人驚嘆。"),
            ("01500", "一千五百章", "Σ(chapters_completed) = 1500", "一千五百章！你已經完成了聖經的很大一部分。"),
            ("01550", "一千五百五十章", "Σ(chapters_completed) = 1550", "一千五百五十章！你的堅持令人感動。"),
            ("01600", "一千六百章", "Σ(chapters_completed) = 1600", "一千六百章！你已經完成了聖經的很大一部分。"),
            ("01650", "一千六百五十章", "Σ(chapters_completed) = 1650", "一千六百五十章！你的進步令人印象深刻。"),
            ("01700", "一千七百章", "Σ(chapters_completed) = 1700", "一千七百章！你已經完成了聖經的很大一部分。"),
            ("01750", "一千七百五十章", "Σ(chapters_completed) = 1750", "一千七百五十章！你的 dedication 令人敬佩。"),
            ("01800", "一千八百章", "Σ(chapters_completed) = 1800", "一千八百章！你正在穩步前進。"),
            ("01850", "一千八百五十章", "Σ(chapters_completed) = 1850", "一千八百五十章！你的進步令人驚嘆。"),
            ("01900", "一千九百章", "Σ(chapters_completed) = 1900", "一千九百章！你已經完成了聖經的很大一部分。"),
            ("01950", "一千九百五十章", "Σ(chapters_completed) = 1950", "一千九百五十章！你的堅持令人感動。"),
            ("01984", "全部完成", "Σ(chapters_completed) = 1984", "恭喜你完成了整本聖經！這是一個令人難以置信的成就。")
        ]
        
        cursor.executemany("""
            INSERT INTO achievement_info (code, name, `condition`, encouragement)
            VALUES (%s, %s, %s, %s)
        """, achievements)
        
        db.commit()
        print("Successfully initialized achievements")
    except Exception as e:
        print(f"Error initializing achievements: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

def init_total_completed_column():
    """Add total_completed column to user_books table if it doesn't exist."""
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Check if column exists
        cursor.execute("SHOW COLUMNS FROM user_books LIKE 'total_completed'")
        if not cursor.fetchone():
            # Add total_completed column
            cursor.execute("ALTER TABLE user_books ADD COLUMN total_completed INT DEFAULT 0")
            db.commit()
            print("Successfully added total_completed column to user_books table")
        else:
            print("total_completed column already exists")
    except Exception as e:
        print(f"Error adding total_completed column: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

def update_user_info_structure():
    """Update the user_info table structure to include new fields."""
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Check and add location column
        cursor.execute("SHOW COLUMNS FROM user_info LIKE 'location'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE user_info ADD COLUMN location VARCHAR(100) DEFAULT NULL")
            
        # Check and add birth_year column
        cursor.execute("SHOW COLUMNS FROM user_info LIKE 'birth_year'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE user_info ADD COLUMN birth_year VARCHAR(4) DEFAULT NULL")
            
        db.commit()
        print("Successfully updated user_info table structure")
    except Exception as e:
        print(f"Error updating user_info structure: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close() 