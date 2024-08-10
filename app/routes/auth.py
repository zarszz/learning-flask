import bcrypt
from flask import Blueprint, g, render_template, redirect, sessions, url_for, flash, request, session
from flask.typing import ResponseReturnValue

from app.models import User, Role
from app import db

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username: str = request.form['username']
        email: str = request.form['email']
        password: str = request.form['password']
        hashed_password: bytes = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        role: Role = Role.query.filter_by(role_name='User').first()
        print(role)
        user: User = User(username=username, email=email, password_hash=hashed_password.decode('utf-8'),
                          role_id=role.id)
        db.session.add(user)
        db.session.commit()

        flash("User registered successfully!", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email: str = request.form['email']
        password: str = request.form['password']

        user: User = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf8'), user.password_hash.encode('utf8')):
            flash("Logged in successfully!")
            session['user_id'] = user.id
            return redirect(url_for('requests.create_request'))
        flash("Login failed. Please try again.")
    return render_template('login.html')


@bp.route('/logout')
def logout() -> ResponseReturnValue:
    session.pop('user_id', None)
    flash("You have been logger out.", 'info')
    return redirect(url_for('main.index'))
