from datetime import datetime
from typing import Optional
from sqlalchemy import Index
from typing import List
from spotto_league.database import db
from spotto_league.models.league_log_detail import LeagueLogDetail
from .base import Base


class LeagueLog(db.Model, Base):

    __tablename__ = 'league_logs'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, nullable=False, index=True)
    user_id_1 = db.Column(db.Integer, nullable=False, index=True)
    user_id_2 = db.Column(db.Integer, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_or_initialize(cls, league_id, user_id_1, user_id_2) -> Optional['LeagueLog']:
        id_1 = user_id_1 if user_id_1 < user_id_2 else user_id_2
        id_2 = user_id_2 if user_id_1 < user_id_2 else user_id_1
        result = db.session.query(cls).\
                filter_by(league_id = league_id, user_id_1 = id_1, user_id_2 = id_2).\
                one_or_none()
        if not result:
            result = cls()
            result.league_id = league_id
            result.user_id_1 = id_1
            result.user_id_2 = id_2
        return result

    @property
    def details(self) -> List[LeagueLogDetail]:
        return db.session.query(LeagueLogDetail).filter_by(league_log_id = self.id).all()

    def is_valid(self, league_id, user_id_1, user_id_2) -> bool:
        id_1 = user_id_1 if user_id_1 < user_id_2 else user_id_2
        id_2 = user_id_2 if user_id_1 < user_id_2 else user_id_1
        return all([self.league_id == league_id,
                    self.user_id_1 == id_1,
                    self.user_id_2 == id_2])

Index('index_user_id_1_and_2', LeagueLog.user_id_1, LeagueLog.user_id_2)
