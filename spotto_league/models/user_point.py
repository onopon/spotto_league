from typing import Optional, List
from datetime import datetime
from spotto_league.database import db
from .base import Base
from spotto_league.models.league import League
from spotto_league.models.league_point import LeaguePoint
from spotto_league.models.bonus_point import BonusPoint
from sqlalchemy import and_


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

    def set_base_point(self, point: int, memo: str = '') -> None:
        self.point = point
        self.reason_class = 'BasePoint'
        self.memo = memo

    def set_league_point(self, league: League, league_point: LeaguePoint) -> None:
        self.point = league_point.point
        self.reason_class = 'LeaguePoint'
        self.reason_id = league.id

    def set_bonus_point(self, bonus_point: BonusPoint) -> None:
        self.point = bonus_point.point
        self.reason_class = 'BonusPoint'
        self.reason_id = bonus_point.id

    def set_point(self, point, reason_class, memo: str = '') -> None:
        self.point = point
        self.reason_class = reason_class
        self.memo = memo

    @classmethod
    def find_all_in_season(self, year: Optional[int] = None) -> List["UserPoint"]:
        if not year:
            year = datetime.today().year
        return db.session.query(UserPoint).filter(and_(
            UserPoint.created_at >= datetime(year, 1, 1, 0, 0, 0),
            UserPoint.created_at <= datetime(year, 12, 31, 23, 59, 59))).all()
