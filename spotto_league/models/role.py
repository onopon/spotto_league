from typing import Optional
from datetime import datetime
from spotto_league.modules.password_util import PasswordUtil
import hashlib
import flask_login
from typing import Dict, Any
from spotto_league.database import db
from .base import Base
from enum import Enum


class RoleType(Enum):
    ADMIN = 1
    MEMBER = 2

    @classmethod
    def all(cls):
        return [{'id': RoleType.ADMIN.value, 'name': '管理者'},
                {'id': RoleType.MEMBER.value, 'name': 'メンバー'}]

class Role(db.Model, Base):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    role_type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_by_user_id(cls, user_id: int) -> Optional['Role']:
        return db.session.query(cls).filter(cls.user_id==user_id).one_or_none()

    @classmethod
    def find_or_initialize_by_user_id(cls, user_id: int) -> 'Role':
        role = Role()
        role.user_id = user_id
        return Role.find_by_user_id(user_id) or role

    def is_admin(self) -> bool:
        return RoleType(self.role_type) == RoleType.ADMIN

    def is_member(self) -> bool:
        return RoleType(self.role_type) == RoleType.MEMBER
