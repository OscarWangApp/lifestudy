from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.database import get_db
import mysql.connector
from functools import wraps

achievement_bp = Blueprint('achievement', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_account') or session.get('user_auth') != '3':
            flash('您沒有權限訪問此頁面', 'danger')
            return redirect(url_for('home.home'))
        return f(*args, **kwargs)
    return decorated_function

@achievement_bp.route('/achievement_management')
@admin_required
def achievement_management():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        # 獲取所有成就信息
        cursor.execute("SELECT * FROM achievement_info ORDER BY code")
        achievements = cursor.fetchall()
        
        # 獲取管理員信息用於顯示
        cursor.execute("SELECT account FROM user_info WHERE auth = '3'")
        admins = [admin['account'] for admin in cursor.fetchall()]
        
        return render_template('achievement_management.html', 
                             achievements=achievements,
                             current_admin=session.get('user_account'),
                             admins=admins)
    except Exception as e:
        print(f"Database error: {e}")
        flash('An error occurred while accessing the database', 'danger')
        return redirect(url_for('home.home'))
    finally:
        cursor.close()
        db.close()

@achievement_bp.route('/add_achievement', methods=['POST'])
@admin_required
def add_achievement():
    code = request.form.get('code')
    name = request.form.get('name')
    condition = request.form.get('condition')
    encouragement = request.form.get('encouragement')
    
    if not all([code, name, condition, encouragement]):
        flash('所有欄位都必須填寫', 'danger')
        return redirect(url_for('achievement.achievement_management'))
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO achievement_info (code, name, `condition`, encouragement)
            VALUES (%s, %s, %s, %s)
        """, (code, name, condition, encouragement))
        db.commit()
        flash('成就添加成功', 'success')
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Duplicate entry error
            flash('成就代碼已存在', 'danger')
        else:
            flash('添加成就失敗', 'danger')
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('achievement.achievement_management'))

@achievement_bp.route('/update_achievement', methods=['POST'])
@admin_required
def update_achievement():
    code = request.form.get('code')
    name = request.form.get('name')
    condition = request.form.get('condition')
    encouragement = request.form.get('encouragement')
    
    if not all([code, name, condition, encouragement]):
        flash('所有欄位都必須填寫', 'danger')
        return redirect(url_for('achievement.achievement_management'))
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            UPDATE achievement_info 
            SET name = %s, `condition` = %s, encouragement = %s
            WHERE code = %s
        """, (name, condition, encouragement, code))
        db.commit()
        flash('成就更新成功', 'success')
    except Exception as e:
        flash('更新成就失敗', 'danger')
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('achievement.achievement_management'))

@achievement_bp.route('/delete_achievement', methods=['POST'])
@admin_required
def delete_achievement():
    code = request.form.get('code')
    
    if not code:
        flash('無效的成就代碼', 'danger')
        return redirect(url_for('achievement.achievement_management'))
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("DELETE FROM achievement_info WHERE code = %s", (code,))
        db.commit()
        flash('成就刪除成功', 'success')
    except Exception as e:
        flash('刪除成就失敗', 'danger')
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('achievement.achievement_management')) 