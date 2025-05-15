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
