from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db


class User(db.Model):
    __tablename__ = 'user'

    def __init__(self, username: str, email: str, password_hash: str, role_id: Optional[int] = None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role_id = role_id

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column()
    role_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey('role.id'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    role: Mapped[Optional['Role']] = relationship('Role', backref='users')


class Role(db.Model):
    __tablename__ = 'role'

    def __init__(self, role_name: str):
        self.role_name = role_name

    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(unique=True, nullable=False)


class Request(db.Model):
    __tablename__ = 'request'

    def __init__(self, requester_id: int, ):
        self.requester_id = requester_id

    id: Mapped[int] = mapped_column(primary_key=True)
    requester_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    status: Mapped[str] = mapped_column(default='pending')
    current_approval_level: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    requester: Mapped['User'] = relationship('User', backref='requests')


class ApprovalLevel(db.Model):
    __tablename__ = 'approval_level'

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(db.ForeignKey('request.id'), nullable=False)
    level: Mapped[int] = mapped_column(nullable=False)
    approver_role_id: Mapped[int] = mapped_column(db.ForeignKey('role.id'), nullable=False)
    status: Mapped[str] = mapped_column(default='pending')
    approved_by: Mapped[Optional[int]] = mapped_column(db.ForeignKey('user.id'))
    approved_at: Mapped[Optional[datetime]] = mapped_column()

    request: Mapped['Request'] = relationship('Request', backref='approval_levels')
    approver_role: Mapped['Role'] = relationship('Role')
    approved_by_user: Mapped[Optional['User']] = relationship('User')
