from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required
from werkzeug.security import generate_password_hash
from .db import get_db
from . import auth_bp

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Get current user info
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE account = ?', (session['user_account'],))
        user = cursor.fetchone()
        
        # Check if username is already taken by another user
        if username != user['username']:
            cursor.execute('SELECT * FROM users WHERE username = ? AND account != ?', 
                         (username, session['user_account']))
            if cursor.fetchone():
                flash('Username is already taken', 'danger')
                return redirect(url_for('auth.profile'))
        
        # Check if email is already taken by another user
        if email != user['email']:
            cursor.execute('SELECT * FROM users WHERE email = ? AND account != ?', 
                         (email, session['user_account']))
            if cursor.fetchone():
                flash('Email is already taken', 'danger')
                return redirect(url_for('auth.profile'))
        
        # Update password if provided
        if password:
            if password != confirm_password:
                flash('Passwords do not match', 'danger')
                return redirect(url_for('auth.profile'))
            hashed_password = generate_password_hash(password)
            cursor.execute('''
                UPDATE users 
                SET username = ?, email = ?, password = ?
                WHERE account = ?
            ''', (username, email, hashed_password, session['user_account']))
        else:
            cursor.execute('''
                UPDATE users 
                SET username = ?, email = ?
                WHERE account = ?
            ''', (username, email, session['user_account']))
        
        get_db().commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('auth.profile'))
    
    # GET request - show profile page
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM users WHERE account = ?', (session['user_account'],))
    user_info = cursor.fetchone()
    
    return render_template('profile.html', user_info=user_info) 