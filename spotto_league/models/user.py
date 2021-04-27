from typing import Optional
from datetime import datetime as dt
from spotto_league.modules.password_util import PasswordUtil
import hashlib
import flask_login
from typing import Dict, Any, List
from spotto_league.database import db
from .base import Base
from .role import Role, RoleType
import datetime
from enum import Enum

class Gender(Enum):
    MALE = 1
    FEMALE = 2


class User(flask_login.UserMixin, db.Model, Base):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.Integer, nullable=False, default=3, index=True)
    birthday = db.Column(db.Date, nullable=False, default=dt.now().date)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=dt.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=dt.now, onupdate=dt.now)
    _role = None

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
        if not self._role:
            self._role = Role.find_by_user_id(self.id)
        return self._role

    def is_admin(self) -> bool:
        if not self._role:
            return False
        return self._role.is_admin()

    def is_member(self) -> bool:
        if not self._role:
            return False
        return self._role.is_member()

    @property
    def birthday_for_display(self) -> str:
        return self.birthday.strftime('%m月%d日')

    @property
    def age(self) -> str:
        today = dt.now()
        age = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age

    @property
    def gender_for_display(self) -> str:
        if (Gender(self.gender) == Gender.MALE):
            return "男性"
        elif (Gender(self.gender) == Gender.FEMALE):
            return "女性"
        return ""
