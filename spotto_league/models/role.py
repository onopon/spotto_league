from typing import Optional, List
from datetime import datetime
from spotto_league.database import db
from .base import Base
from enum import Enum


class RoleType(Enum):
    GUEST = 0  # ゲスト。メンバーになる可能性がある人。ポイント付与なし。
    ADMIN = 1  # 管理者
    MEMBER = 2  # メンバー
    VISITOR = 3  # ビジター。機能が制限されている。

    @classmethod
    def all(cls):
        # GUEST と VISITOR は特別枠なので、allには含めない。
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
    def all(cls) -> List['Role']:
        return db.session.query(Role).all()

    @classmethod
    def find_by_user_id(cls, user_id: int) -> Optional['Role']:
        return db.session.query(cls).filter(cls.user_id == user_id).one_or_none()

    @classmethod
    def find_or_initialize_by_user_id(cls, user_id: int) -> 'Role':
        role = Role()
        role.user_id = user_id
        role.role_type = RoleType.GUEST.value
        return Role.find_by_user_id(user_id) or role

    def is_admin(self) -> bool:
        return RoleType(self.role_type) == RoleType.ADMIN

    def is_member(self) -> bool:
        return RoleType(self.role_type) == RoleType.MEMBER

    def is_guest(self) -> bool:
        return RoleType(self.role_type) == RoleType.GUEST

    def is_visitor(self) -> bool:
        return RoleType(self.role_type) == RoleType.VISITOR
