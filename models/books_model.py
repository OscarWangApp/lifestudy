import json
from models.database import get_db
        
def get_books_info():
    """Fetch all books from books_info table and return as a list of dictionaries."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books_info order by `sql` asc")
    books_info = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description] #get column names.
    
    result = []
    for row in books_info:
        row_dict = {}
        for i, value in enumerate(row):
            row_dict[columns[i]] = value
        result.append(row_dict)

    return result  # Return Python list of dictionaries instead of JSON string
