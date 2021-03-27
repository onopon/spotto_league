from typing import List
from datetime import datetime
from spotto_league.database import db
from .base import Base

RATING_BORDER_MEMBER_COUNT = 12
BASE_GROUP_ID = 1
ONE_AND_HALF_TIMES_GROUP_ID = 2
TWO_TIMES_GROUP_ID = 3


class LeaguePoint(db.Model, Base):

    __tablename__ = 'league_points'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False, index=True)
    rank = db.Column(db.Integer, nullable=False)
    point = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_all_by_group_id(cls, group_id: int) -> List['LeaguePoint']:
        return db.session.query(cls).filter(cls.group_id == group_id).all()
