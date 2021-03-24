from datetime import datetime
from spotto_league.database import db
from .base import Base


class LeaguePoint(db.Model, Base):

    __tablename__ = 'league_points'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False, index=True)
    rank = db.Column(db.Integer, nullable=False)
    point = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
