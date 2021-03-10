from datetime import datetime
from spotto_league.database import db
from sqlalchemy import Index
from typing import List
from spotto_league.database import SpottoDB
from spotto_league.models.league_log_detail import LeagueLogDetail


class LeagueLog(db.Model):

    __tablename__ = 'league_logs'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, nullable=False, index=True)
    user_id_1 = db.Column(db.Integer, nullable=False, index=True)
    user_id_2 = db.Column(db.Integer, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @property
    def details(self) -> List[LeagueLogDetail]:
        return SpottoDB().session.query(LeagueLogDetail).\
            filter_by(league_log_id = self.id).all()

Index('index_user_id_1_and_2', LeagueLog.user_id_1, LeagueLog.user_id_2)
