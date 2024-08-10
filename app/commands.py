import bcrypt
from flask import Blueprint

from app.db import db
from app.models import Role

bp = Blueprint('commands', __name__)


@bp.cli.command('seed_roles')
def seed_roles():
    db.create_all()

    # create default roles
    roles = ['Admin', 'Approver', 'User']
    for name in roles:
        role = Role(role_name=name)
        db.session.add(role)

    db.session.commit()
    print("Roles seeded successfully!")


@bp.cli.command('seed_users')
def seed_users():
    from app.models import User
    from app.models import Role

    default_password = 'password'
    hashed_password: bytes = bcrypt.hashpw(default_password.encode('utf8'), bcrypt.gensalt())

    db.create_all()

    # create user with User role
    user_role = Role.query.filter_by(role_name='User').first()
    user_user = User(username='user', role_id=user_role.id, email='user@gmail.com',
                     password_hash=hashed_password.decode('utf8'))
    db.session.add(user_user)

    # create user with Approver role
    approver_role = Role.query.filter_by(role_name='Approver').first()
    approver_user = User(username='approver', role_id=approver_role.id, email='approver@gmail.com',
                         password_hash=hashed_password.decode('utf8'))
    db.session.add(approver_user)

    # create user with Admin role
    admin_role = Role.query.filter_by(role_name='Admin').first()
    admin_user = User(username='admin', role_id=admin_role.id, email='admin@gmail.com',
                      password_hash=hashed_password.decode('utf8'))
    db.session.add(admin_user)

    db.session.commit()
    print("Users seeded successfully!")