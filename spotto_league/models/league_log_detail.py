from datetime import datetime
from .base import Base
from spotto_league.database import db
from typing import List


class LeagueLogDetail(db.Model, Base):

    __tablename__ = 'league_log_details'

    id = db.Column(db.Integer, primary_key=True)
    league_log_id = db.Column(db.Integer, nullable=False, index=True)
    score_1 = db.Column(db.Integer, nullable=False)
    score_2 = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def is_zero_all(self):
        return all([self.score_1 == 0, self.score_2 == 0])

    @classmethod
    def find_all_by_league_log_ids(cls, league_log_ids: List[int]) -> List['LeagueLogDetail']:
        return db.session.query(cls).filter(cls.league_log_id.in_(league_log_ids)).all()
