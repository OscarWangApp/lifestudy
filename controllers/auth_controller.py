from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db
from models.user_model import get_locations, get_user_by_account, add_user
from models.books_model import get_books_info
import mysql.connector

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        user = get_user_by_account(account)
        if user and check_password_hash(user['password'], password):
            session['user_account'] = user['account']
            session['user_auth'] = user['auth']  # 將用戶的 auth 值存入 session
            return redirect(url_for('home.home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_account', None)
    session.pop('user_auth', None)  # 清除 auth session
    return redirect(url_for('home.home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    locations = get_locations()

    if request.method == 'GET':        
        return render_template('register.html', locations=locations)
    else:
        account = request.form['account']
        password = request.form['password']
        location = request.form['city']+'-'+request.form['hall']+'-'+request.form['district']
        birth_year = request.form['birth_year']
        achievement = ''  # default as none
        auth = '1'  # 設置預設的 auth 值為 "1"
        hashed_password = generate_password_hash(password)
        
        try:
            # 獲取書籍信息
            books_info = get_books_info()
            # 使用新的add_user函數，一次性完成用戶註冊和書籍初始化
            add_user(account, hashed_password, location, birth_year, achievement, books_info)
            # 註冊成功後自動登入
            session['user_account'] = account
            session['user_auth'] = auth  # 設置新註冊用戶的 auth session
            return redirect(url_for('home.home'))
        except mysql.connector.Error as e:
            if e.errno == 1062:  # Duplicate entry error
                return render_template('register.html', error='Account already taken', locations=locations)
            else:
                print(f"Registration error: {e}")
                return render_template('register.html', error='Registration failed. Please try again.', locations=locations)
        except Exception as e:
            print(f"Registration error: {e}")
            return render_template('register.html', error='Registration failed. Please try again.', locations=locations)
        
@auth_bp.route('/check_account')
def check_account():
    account = request.args.get('account')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS count FROM user_info WHERE account = %s", (account,))
    result = cursor.fetchone()
    return {"exists": result["count"] > 0}

@auth_bp.route('/user_management')
def user_management():
    # 檢查用戶是否登錄且具有管理員權限
    if not session.get('user_account') or session.get('user_auth') != '3':
        return redirect(url_for('home.home'))
    
    # 獲取所有用戶信息
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT account, location, birth_year, achievement, auth FROM user_info ORDER BY account")
    users = cursor.fetchall()
    
    return render_template('user_management.html', users=users)

@auth_bp.route('/update_auth', methods=['POST'])
def update_auth():
    # 檢查用戶是否登錄且具有管理員權限
    if not session.get('user_account') or session.get('user_auth') != '3':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    account = data.get('account')
    new_auth = data.get('auth')
    
    # 不允許管理員修改自己的權限
    if account == session.get('user_account'):
        return jsonify({'success': False, 'error': 'Cannot modify own auth level'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE user_info SET auth = %s WHERE account = %s", (new_auth, account))
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating auth: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/delete_user', methods=['POST'])
def delete_user():
    # 檢查用戶是否登錄且具有管理員權限
    if not session.get('user_account') or session.get('user_auth') != '3':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    account = data.get('account')
    
    # 不允許管理員刪除自己的帳號
    if account == session.get('user_account'):
        return jsonify({'success': False, 'error': 'Cannot delete own account'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        # 開始事務
        cursor.execute("BEGIN")
        
        # 刪除用戶的書籍記錄
        cursor.execute("DELETE FROM user_books WHERE account = %s", (account,))
        
        # 刪除用戶信息
        cursor.execute("DELETE FROM user_info WHERE account = %s", (account,))
        
        # 提交事務
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting user: {e}")
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('user_account'):
        return redirect(url_for('auth.login'))
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        if request.method == 'POST':
            location = request.form.get('city')+'-'+request.form.get('hall')+'-'+request.form.get('district')
            birth_year = request.form.get('birth_year')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Get current user info
            cursor.execute('SELECT * FROM user_info WHERE account = %s', (session['user_account'],))
            user = cursor.fetchone()
            
            # Update user information
            update_fields = []
            update_values = []
            
            if location:
                update_fields.append('location = %s')
                update_values.append(location)
            if birth_year:
                update_fields.append('birth_year = %s')
                update_values.append(birth_year)
            
            # Update password only if provided (checkbox was checked)
            if password:
                if password != confirm_password:
                    flash('Passwords do not match', 'danger')
                    return redirect(url_for('auth.profile'))
                hashed_password = generate_password_hash(password)
                update_fields.append('password = %s')
                update_values.append(hashed_password)
            
            if update_fields:
                update_values.append(session['user_account'])
                query = f'''
                    UPDATE user_info 
                    SET {', '.join(update_fields)}
                    WHERE account = %s
                '''
                cursor.execute(query, update_values)
                db.commit()
                flash('Profile updated successfully', 'success')
            else:
                flash('No changes were made', 'info')
            
            return redirect(url_for('auth.profile'))
        
        # GET request - show profile page
        cursor.execute('SELECT account, location, birth_year FROM user_info WHERE account = %s', (session['user_account'],))
        user_info = cursor.fetchone()
        
        # Split location into components
        current_location = user_info['location'].split('-') if user_info['location'] else ['', '', '']
        current_city = current_location[0] if len(current_location) > 0 else ''
        current_hall = current_location[1] if len(current_location) > 1 else ''
        current_district = current_location[2] if len(current_location) > 2 else ''
        
        # Get locations for the dropdowns
        locations = get_locations()

        # Get user's progress statistics
        cursor.execute('''
            SELECT total_completed 
            FROM user_books 
            WHERE account = %s
        ''', (session['user_account'],))
        user_progress = cursor.fetchone()
        total_completed = user_progress['total_completed'] if user_progress else 0

        # Get number of users who completed all chapters in the same location
        cursor.execute('''
            SELECT COUNT(*) as completed_count
            FROM user_books ub
            WHERE ub.total_completed = 1984
        ''')
        location_completed = cursor.fetchone()['completed_count']

        # Calculate completed achievements
        cursor.execute('''
            SELECT COUNT(*) as completed_count
            FROM achievement_info
            WHERE CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(`condition`, '=', -1), ' ', -1) AS UNSIGNED) <= %s
        ''', (total_completed,))
        completed_achievements = cursor.fetchone()['completed_count']

        # Get next achievement
        cursor.execute('''
            SELECT code, name, `condition`, encouragement
            FROM achievement_info
            WHERE CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(`condition`, '=', -1), ' ', -1) AS UNSIGNED) > %s
            ORDER BY CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(`condition`, '=', -1), ' ', -1) AS UNSIGNED)
            LIMIT 1
        ''', (total_completed,))
        next_achievement = cursor.fetchone()
        
        if next_achievement:
            next_target = int(next_achievement['condition'].split('=')[1].strip())
            cursor.execute('''
                SELECT COUNT(*) as next_completed_count
                FROM user_books ub
                WHERE ub.total_completed >= %s
            ''', (next_target,))
            location_next_completed = cursor.fetchone()['next_completed_count']
        else:
            location_next_completed = 0
        
        return render_template('profile.html', 
                             user_info=user_info, 
                             locations=locations,
                             current_city=current_city,
                             current_hall=current_hall,
                             current_district=current_district,
                             total_completed=total_completed,
                             location_completed=location_completed,
                             next_achievement=next_achievement,
                             location_next_completed=location_next_completed,
                             completed_achievements=completed_achievements)
        
    except Exception as e:
        print(f"Database error: {e}")
        flash('An error occurred while accessing the database', 'danger')
        return redirect(url_for('home.home'))
        
    finally:
        cursor.close()
        db.close()