from typing import Optional, List
from datetime import datetime
from spotto_league.database import db
from .base import Base
from .user import User


class BonusPoint(db.Model, Base):

    __tablename__ = "bonus_points"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    point = db.Column(db.Integer, nullable=False)
    available_count = db.Column(db.Integer, nullable=False, default=4)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    _user = None

    @classmethod
    def all(cls) -> List["BonusPoint"]:
        return db.session.query(BonusPoint).all()

    @classmethod
    def find_by_user_id(cls, user_id: int) -> Optional["BonusPoint"]:
        return db.session.query(cls).filter(cls.user_id == user_id).one_or_none()

    @classmethod
    def find_or_initialize_by_user_id(cls, user_id: int) -> "BonusPoint":
        bonus_point = cls()
        bonus_point.user_id = user_id
        return cls.find_by_user_id(user_id) or bonus_point

    @classmethod
    def find_all_by_user_ids(cls, user_ids: List[int]) -> List["BonusPoint"]:
        return db.session.query(cls).filter(cls.user_id.in_(user_ids)).all()

    @property
    def user(self) -> User:
        if not self._user:
            self._user = User.find(self.user_id)
        return self._user
