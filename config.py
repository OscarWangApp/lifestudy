class Config:
    # Database configuration
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "1234"
    DB_NAME = "lifestudy"
    
    # Alternative database configuration (commented out)
    # DB_HOST = "OscarWang.mysql.pythonanywhere-services.com"
    # DB_USER = "OscarWang"
    # DB_PASSWORD = "lifestudy"
    # DB_NAME = "OscarWang$lifestudy"
    
    # Flask configuration
    SECRET_KEY = 'your-secret-key'  # 請更換為安全的密鑰