from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, get_db

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.form
    username = data.get('username')
    password = data.get('password')
    db = get_db()
    user = db.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', error='認証失敗')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
