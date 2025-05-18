from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from models.database import get_db
from functools import wraps

location_bp = Blueprint('location', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_account') or session.get('user_auth') != '3':
            flash('您沒有權限訪問此頁面', 'danger')
            return redirect(url_for('home.home'))
        return f(*args, **kwargs)
    return decorated_function

@location_bp.route('/')
@admin_required
def location_management():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM location_info ORDER BY church, district, hall")
        locations = cursor.fetchall()
        return render_template('location_management.html', locations=locations)
    except Exception as e:
        print(f"Database error: {e}")
        flash('獲取位置信息時發生錯誤', 'danger')
        return redirect(url_for('home.home'))
    finally:
        cursor.close()
        db.close()

@location_bp.route('/add', methods=['POST'])
@admin_required
def add_location():
    data = request.get_json()
    church = data.get('church')
    district = data.get('district')
    hall = data.get('hall')
    
    if not all([church, district, hall]):
        return jsonify({'success': False, 'error': '所有欄位都必須填寫'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO location_info (church, district, hall) VALUES (%s, %s, %s)", 
                      (church, district, hall))
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error adding location: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@location_bp.route('/update', methods=['POST'])
@admin_required
def update_location():
    data = request.get_json()
    location_id = data.get('id')
    church = data.get('church')
    district = data.get('district')
    hall = data.get('hall')
    
    if not all([location_id, church, district, hall]):
        return jsonify({'success': False, 'error': '所有欄位都必須填寫'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE location_info SET church = %s, district = %s, hall = %s WHERE id = %s",
                      (church, district, hall, location_id))
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating location: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@location_bp.route('/delete', methods=['POST'])
@admin_required
def delete_location():
    data = request.get_json()
    location_id = data.get('id')
    
    if not location_id:
        return jsonify({'success': False, 'error': '無效的位置ID'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM location_info WHERE id = %s", (location_id,))
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting location: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        db.close() 