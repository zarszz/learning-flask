from functools import wraps

from flask import session, flash, redirect, url_for
from flask.typing import ResponseReturnValue

from app.models import User


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need logged in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function


def role_required(role_name: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs) -> ResponseReturnValue:
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            if user.role.role_name != role_name:
                flash('You do not have permission to access this page.', 'warning')
                return redirect(url_for('main.index'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
