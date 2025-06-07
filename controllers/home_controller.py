from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from models.books_model import get_books_info
from models.home_model import get_book_content
from models.database import get_db
from models.user_model import get_user_progress
import json

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    user_account = session.get('user_account')

    if user_account:
        # Get books info for the selector
        books_info = get_books_info()
        
        # 確保所有值都是可序列化的
        serializable_books = []
        for book in books_info:
            serializable_book = {
                'id': book.get('id'),
                'name': book.get('name'),
                'code': book.get('code'),
                'chapter': book.get('chapter'),
                'sql': book.get('sql')
            }
            serializable_books.append(serializable_book)
        
        # 將 books_info 轉換為 JSON 字符串
        books_info_json = json.dumps(serializable_books)
        
        # Get user progress information
        user_progress = get_user_progress(user_account)
        
        # Get last reading position and book progress
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get last_tag
        cursor.execute("SELECT last_tag FROM user_books WHERE account = %s", (user_account,))
        result = cursor.fetchone()
        last_tag = result['last_tag'] if result else None
        
        # Convert last_tag to display format if it exists
        last_reading = None
        if last_tag:
            book_code, chapter = last_tag.split('-')
            # Find the book name from books_info
            for book in serializable_books:
                if book['code'].lower() == book_code:
                    last_reading = f"{book['name']} 第{chapter}篇"
                    break
        
        # Calculate progress for each book
        book_progress = []
        for book in serializable_books:
            book_code = book['code'].lower()
            cursor.execute(f"SELECT {book_code} FROM user_books WHERE account = %s", (user_account,))
            result = cursor.fetchone()
            if result:
                status = result[book_code]
                total_chapters = book['chapter']
                completed = status.count('1')
                progress = (completed / total_chapters) * 100 if total_chapters > 0 else 0
                book_progress.append({
                    'name': book['name'],
                    'progress': progress,
                    'completed': completed,
                    'total': total_chapters
                })
        
        # Find the book closest to 100% completion
        closest_book = None
        if book_progress:
            # Sort by progress in descending order
            book_progress.sort(key=lambda x: x['progress'], reverse=True)
            # Get the book with highest progress
            closest_book = book_progress[0]
        
        # User is logged in, display the home page with user account information
        return render_template('home.html', 
                            user_account=user_account, 
                            books=serializable_books,
                            user_progress=user_progress,
                            last_reading=last_reading,
                            last_tag=last_tag,
                            closest_book=closest_book)
    else:
        # User is not logged in, redirect to login page
        return redirect(url_for('auth.login'))

@home_bp.route('/get_book_content', methods=['GET'])
def get_content():
    # 檢查用戶是否已登入
    if not session.get('user_account'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    # 獲取請求參數
    book_sql = request.args.get('sql')
    book_code = request.args.get('code')
    chapter = request.args.get('chapter')
    
    # 驗證參數
    if not all([book_sql, book_code, chapter]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    # 獲取書籍內容
    content = get_book_content(book_sql, book_code, chapter)
    
    if content is None:
        return jsonify({'error': 'Content not found', 'content': ''}), 404
    
    # 返回內容
    return jsonify({
        'content': content,
        'title': f"{book_code} 第{chapter}章",
        'completed': False  # 默認值
    })

@home_bp.route('/get_chapters/<book_code>', methods=['GET'])
def get_chapters(book_code):
    if not session.get('user_account'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not book_code or book_code == 'null':
        return jsonify({'error': 'Invalid book code'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 獲取書籍信息
        cursor.execute("SELECT * FROM books_info WHERE code = %s", (book_code,))
        book = cursor.fetchone()
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # 獲取用戶的閱讀記錄
        book_column = book['code'].lower()
        cursor.execute(f"SELECT {book_column} FROM user_books WHERE account = %s", (session['user_account'],))
        result = cursor.fetchone()
        
        if not result:
            # 如果沒有閱讀記錄，創建一個新的記錄
            cursor.execute(f"""
                INSERT INTO user_books (account, {book_column})
                VALUES (%s, %s)
            """, (session['user_account'], '0' * book['chapter']))
            db.commit()
            
            # 重新獲取記錄
            cursor.execute(f"SELECT {book_column} FROM user_books WHERE account = %s", (session['user_account'],))
            result = cursor.fetchone()
        
        # 構建章節列表
        chapters = []
        status = result[book_column]
        for i in range(book['chapter']):
            chapters.append({
                'chapter_number': i + 1,
                'completed': status[i] == '1' if i < len(status) else False
            })
        
        return jsonify({'chapters': chapters})
    except Exception as e:
        print(f"Error getting chapters: {e}")
        return jsonify({'error': str(e)}), 500

@home_bp.route('/get_chapter_content/<book_code>/<chapter_number>', methods=['GET'])
def get_chapter_content(book_code, chapter_number):
    if not session.get('user_account'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not book_code or book_code == 'null':
        return jsonify({'error': 'Invalid book code'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 獲取書籍信息
        cursor.execute("SELECT * FROM books_info WHERE code = %s", (book_code,))
        book = cursor.fetchone()
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # 獲取章節內容
        content = get_book_content(book['sql'], book['code'], chapter_number)
        
        if content is None:
            return jsonify({'error': 'Content not found', 'content': ''}), 404
        
        # 獲取章節完成狀態
        book_column = book['code'].lower()
        cursor.execute(f"SELECT {book_column} FROM user_books WHERE account = %s", (session['user_account'],))
        result = cursor.fetchone()
        
        completed = False
        if result and result[book_column]:
            chapter_index = int(chapter_number) - 1
            if chapter_index < len(result[book_column]):
                completed = result[book_column][chapter_index] == '1'
        
        response_data = {
            'title': f"{book['name']} 第{chapter_number}篇",
            'content': content,
            'completed': completed
        }
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@home_bp.route('/get_chapter_status', methods=['GET'])
def get_chapter_status():
    if not session.get('user_account'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    book_code = request.args.get('code')
    chapter = request.args.get('chapter')
    
    if not all([book_code, chapter]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        # 獲取用戶的閱讀記錄
        book_column = book_code.lower()
        print(f"Checking status for user {session['user_account']}, book {book_column}, chapter {chapter}")
        
        cursor.execute(f"SELECT {book_column} FROM user_books WHERE account = %s", (session['user_account'],))
        result = cursor.fetchone()
        
        if not result:
            print(f"No reading record found for user {session['user_account']}")
            return jsonify({'error': 'User reading record not found'}), 404
        
        # 獲取章節狀態
        chapter_index = int(chapter) - 1  # 轉換為0-based索引
        chapter_status = result[0][chapter_index] if chapter_index < len(result[0]) else '0'
        
        print(f"Chapter status: {chapter_status}, is_completed: {chapter_status == '1'}")
        return jsonify({'is_completed': chapter_status == '1'})
    except Exception as e:
        print(f"Error getting chapter status: {e}")
        return jsonify({'error': str(e)}), 500

@home_bp.route('/mark_chapter_complete', methods=['POST'])
def mark_chapter_complete():
    if not session.get('user_account'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    book_code = data.get('book_code')
    chapter = data.get('chapter_number')
    
    if not all([book_code, chapter]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        # 開始事務
        cursor.execute("BEGIN")
        
        # 獲取當前的閱讀記錄
        book_column = book_code.lower()
        print(f"Marking chapter complete for user {session['user_account']}, book {book_column}, chapter {chapter}")
        
        cursor.execute(f"SELECT {book_column}, total_completed FROM user_books WHERE account = %s", (session['user_account'],))
        result = cursor.fetchone()
        
        if not result:
            print(f"No reading record found for user {session['user_account']}")
            return jsonify({'error': 'User reading record not found'}), 404
        
        # 更新章節狀態
        chapter_index = int(chapter) - 1  # 轉換為0-based索引
        current_status = list(result[0])
        current_total = result[1] or 0
        
        print(f"Current status: {result[0]}, chapter index: {chapter_index}")
        
        if chapter_index < len(current_status):
            # 如果章節還沒完成，增加總完成數
            if current_status[chapter_index] != '1':
                current_total += 1
            
            current_status[chapter_index] = '1'
            new_status = ''.join(current_status)
            
            print(f"New status: {new_status}")
            
            # 更新數據庫 - 同時更新章節狀態、last_tag和total_completed
            new_last_tag = f"{book_code.lower()}-{chapter}"
            cursor.execute(f"""
                UPDATE user_books 
                SET {book_column} = %s, 
                    last_tag = %s,
                    total_completed = %s,
                    last_time = NOW()
                WHERE account = %s
            """, (new_status, new_last_tag, current_total, session['user_account']))
            
            # 獲取所有成就
            cursor.execute("SELECT code, `condition` FROM achievement_info ORDER BY code")
            achievements = cursor.fetchall()
            
            # 找到符合條件的最高成就
            highest_achievement = None
            for achievement in achievements:
                code, condition = achievement
                # 從條件中提取數字
                required_chapters = int(condition.split('=')[1].strip())
                if current_total >= required_chapters:
                    highest_achievement = code
            
            # 如果找到符合的成就，更新用戶的成就
            if highest_achievement:
                cursor.execute("""
                    UPDATE user_info 
                    SET achievement = %s 
                    WHERE account = %s
                """, (highest_achievement, session['user_account']))
            
            # 提交事務
            db.commit()
            return jsonify({'success': True})
        else:
            print(f"Invalid chapter number: {chapter_index}, status length: {len(current_status)}")
            return jsonify({'error': 'Invalid chapter number'}), 400
    except Exception as e:
        print(f"Error marking chapter complete: {e}")
        db.rollback()
        return jsonify({'error': str(e)}), 500

@home_bp.route('/get_book_status', methods=['GET'])
def get_book_status():
    if not session.get('user_account'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    book_code = request.args.get('code')
    
    if not book_code:
        return jsonify({'error': 'Missing book code'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        # 獲取用戶的閱讀記錄
        book_column = book_code.lower()
        cursor.execute(f"SELECT {book_column} FROM user_books WHERE account = %s", (session['user_account'],))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'error': 'User reading record not found'}), 404
        
        # 返回所有章節的狀態
        chapters = list(result[0])
        return jsonify({'chapters': chapters})
    except Exception as e:
        print(f"Error getting book status: {e}")
        return jsonify({'error': str(e)}), 500

@home_bp.route('/get_user_progress', methods=['GET'])
def get_user_progress_ajax():
    if not session.get('user_account'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Get books info
        books_info = get_books_info()
        
        # Get user progress information
        user_progress = get_user_progress(session['user_account'])
        
        # Get last reading position and book progress
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get last_tag
        cursor.execute("SELECT last_tag FROM user_books WHERE account = %s", (session['user_account'],))
        result = cursor.fetchone()
        last_tag = result['last_tag'] if result else None
        
        # Convert last_tag to display format if it exists
        last_reading = None
        if last_tag:
            book_code, chapter = last_tag.split('-')
            # Find the book name from books_info
            for book in books_info:
                if book['code'].lower() == book_code:
                    last_reading = f"{book['name']} 第{chapter}篇"
                    break
        
        # Calculate progress for each book
        book_progress = []
        for book in books_info:
            book_code = book['code'].lower()
            cursor.execute(f"SELECT {book_code} FROM user_books WHERE account = %s", (session['user_account'],))
            result = cursor.fetchone()
            if result:
                status = result[book_code]
                total_chapters = book['chapter']
                completed = status.count('1')
                progress = (completed / total_chapters) * 100 if total_chapters > 0 else 0
                book_progress.append({
                    'name': book['name'],
                    'progress': progress,
                    'completed': completed,
                    'total': total_chapters
                })
        
        # Find the book closest to 100% completion
        closest_book = None
        if book_progress:
            # Sort by progress in descending order
            book_progress.sort(key=lambda x: x['progress'], reverse=True)
            # Get the book with highest progress
            closest_book = book_progress[0]
        
        return jsonify({
            'total_completed': user_progress['total_completed'],
            'next_achievement': user_progress['next_achievement'],
            'last_reading': last_reading,
            'closest_book': closest_book
        })
    except Exception as e:
        print(f"Error getting user progress: {e}")
        return jsonify({'error': str(e)}), 500

@home_bp.route('/unmark_chapter_complete', methods=['POST'])
def unmark_chapter_complete():
    if not session.get('user_account'):
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    book_code = data.get('book_code')
    chapter = data.get('chapter_number')

    if not all([book_code, chapter]):
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("BEGIN")

        book_column = book_code.lower()
        cursor.execute(f"SELECT {book_column}, total_completed FROM user_books WHERE account = %s", (session['user_account'],))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'User reading record not found'}), 404

        chapter_index = int(chapter) - 1
        current_status = list(result[0])
        current_total = result[1] or 0

        if chapter_index < len(current_status):
            if current_status[chapter_index] == '1':
                current_total = max(0, current_total - 1)
            current_status[chapter_index] = '0'
            new_status = ''.join(current_status)

            cursor.execute(f"""
                UPDATE user_books 
                SET {book_column} = %s, 
                    total_completed = %s,
                    last_time = NOW()
                WHERE account = %s
            """, (new_status, current_total, session['user_account']))

            db.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Invalid chapter number'}), 400
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@home_bp.route('/update_last_reading', methods=['POST'])
def update_last_reading():
    if not session.get('user_account'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    book_code = data.get('book_code')
    chapter_number = data.get('chapter_number')
    
    if not all([book_code, chapter_number]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        # 更新用戶的最後閱讀位置
        last_tag = f"{book_code.lower()}-{chapter_number}"
        cursor.execute("""
            UPDATE user_books 
            SET last_tag = %s,
                last_time = NOW()
            WHERE account = %s
        """, (last_tag, session['user_account']))
        
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating last reading: {e}")
        db.rollback()
        return jsonify({'error': str(e)}), 500