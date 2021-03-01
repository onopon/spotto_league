from datetime import datetime
from spotto_league.database import db


class LeagueMember(db.Model):

    __tablename__ = 'league_members'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
