from typing import Optional
from datetime import datetime
from spotto_league.modules.password_util import PasswordUtil
import hashlib
import flask_login
from typing import Dict, Any, List
from spotto_league.database import db
from .base import Base
from .role import Role


class User(flask_login.UserMixin, db.Model, Base):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def set_password(self, password: str) -> None:
        self.password = PasswordUtil.make_hex(password)

    @classmethod
    def all(cls) -> List['User']:
        return db.session.query(User).all()

    @classmethod
    def find_by_login_name(cls, login_name) -> Optional['User']:
        return db.session.query(cls).filter(cls.login_name==login_name).one_or_none()

    def to_hash(self) -> Dict[str ,Any]:
        return {'id': self.id,
                'login_name': self.login_name,
                'name': self.name}

    @property
    def role(self) -> Optional[Role]:
        return Role.find_by_user_id(self.id)

    def is_admin(self) -> bool:
        role = self.role
        if not role:
            return False
        return role.is_admin()
