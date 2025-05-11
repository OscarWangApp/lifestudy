from flask import Blueprint, render_template
from models.database import get_db
from models.user_model import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def manage_users():
    users = User.query.all()
    return render_template('user_management.html', users=users)