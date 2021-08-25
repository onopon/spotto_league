from typing import List
from datetime import datetime
from spotto_league.database import db
from .base import Base


class Unpaid(db.Model, Base):

    __tablename__ = "unpaids"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    amount = db.Column(db.Integer, nullable=False)
    memo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    @classmethod
    def all(cls) -> List["Unpaid"]:
        return db.session.query(cls).all()
