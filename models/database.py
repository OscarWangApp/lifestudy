import mysql.connector
from config import Config

def get_db():
    """Establish and return a database connection."""
    db = mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
        #host="OscarWang.mysql.pythonanywhere-services.com",
        #user="OscarWang",
        #password="lifestudy",
        #database="OscarWang$lifestudy"
    )
    return db 