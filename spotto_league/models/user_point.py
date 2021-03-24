from datetime import datetime
from spotto_league.database import db
from .base import Base


class UserPoint(db.Model, Base):

    __tablename__ = 'user_points'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    league_id = db.Column(db.Integer, index=True)
    point = db.Column(db.Integer, nullable=False)
    reason_class = db.Column(db.String(255))
    reason_id = db.Column(db.Integer)
    memo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
