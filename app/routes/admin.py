from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import db, User, Role
from app.decorators import login_required, role_required
from flask.typing import ResponseReturnValue
from typing import List

bp: Blueprint = Blueprint('admin', __name__)


@bp.route('/admin/users', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def manage_users() -> ResponseReturnValue:
    if request.method == 'POST':
        user_id: int = int(request.form['user_id'])
        role_id: int = int(request.form['role_id'])

        user = User.query.get(user_id)
        if user.role.role_name == 'Admin':
            flash('You cannot update the role of an Admin user.', 'danger')
            return redirect(url_for('admin.manage_users'))
        
        user.role_id = role_id
        db.session.commit()

        flash('User role updated successfully!', 'success')
        return redirect(url_for('admin.manage_users'))
    else:
        users: List[User] = User.query.all()
        roles: List[Role] = Role.query.all()
        return render_template('manage_users.html', users=users, roles=roles)
