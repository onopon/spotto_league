from typing import Optional
from datetime import datetime
from spotto_league.modules.password_util import PasswordUtil
import hashlib
import flask_login
from typing import Dict, Any
from spotto_league.database import SpottoDB
from .base import Base
from enum import Enum

db = SpottoDB()


class RoleType(Enum):
    ADMIN = 1

class Role(db.Model, Base):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    role_type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_by_user_id(cls, user_id: int) -> Optional['Role']:
        return SpottoDB().session.query(cls).filter(cls.user_id==user_id).one_or_none()

    @classmethod
    def find_or_initialize_by_user_id(cls, user_id: int) -> 'Role':
        role = Role()
        role.user_id = user_id
        return Role.find_by_id(user_id) or role

    def is_admin(self) -> bool:
        return RoleType(self.role_type) == RoleType.ADMIN
