from datetime import datetime
from spotto_league.database import db


class LeagueLog(db.Model):

    __tablename__ = 'league_logs'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, nullable=False)
    user_id_1 = db.Column(db.Integer, nullable=False)
    user_id_2 = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
