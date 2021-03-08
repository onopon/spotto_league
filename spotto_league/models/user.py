from typing import Optional
from datetime import datetime
from spotto_league.database import db
from spotto_league.modules.password_util import PasswordUtil
import hashlib
import flask_login


class User(db.Model):

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
    def find_by_login_name(cls, session, login_name) -> Optional['User']:
        return session.query(cls).filter(cls.login_name==login_name).one_or_none()
