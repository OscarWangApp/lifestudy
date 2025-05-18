from flask import Blueprint, render_template, redirect, url_for, session, flash
from models.database import get_db
from functools import wraps

user_bp = Blueprint('user', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_account') or session.get('user_auth') != '3':
            flash('您沒有權限訪問此頁面', 'danger')
            return redirect(url_for('home.home'))
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/')
@admin_required
def manage_users():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_info ORDER BY account")
        users = cursor.fetchall()
        return render_template('user_management.html', users=users)
    except Exception as e:
        print(f"Database error: {e}")
        flash('獲取用戶信息時發生錯誤', 'danger')
        return redirect(url_for('home.home'))
    finally:
        cursor.close()
        db.close()