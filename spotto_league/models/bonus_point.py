from typing import Optional
from datetime import datetime
from spotto_league.database import db
from .base import Base


class BonusPoint(db.Model, Base):

    __tablename__ = 'bonus_points'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    point = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_by_user_id(cls, user_id: int) -> Optional['BonusPoint']:
        return db.session.query(cls).filter(cls.user_id==user_id).one_or_none()

    @classmethod
    def find_or_initialize_by_user_id(cls, user_id: int) -> 'BonusPoint':
        bonus_point = cls()
        bonus_point.user_id = user_id
        return cls.find_by_id(user_id) or bonus_point
