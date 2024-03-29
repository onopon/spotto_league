import sqlalchemy as sa
from typing import List
from datetime import datetime
from spotto_league.database import db
from .user import User
from .base import Base


class LeagueMember(db.Model, Base):

    __tablename__ = "league_members"

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    _user = None

    @property
    def user(self) -> User:
        if not self._user:
            self._user = User.find(self.user_id)
        return self._user

    @classmethod
    def find_all_by_league_id(cls, league_id: int) -> List["LeagueMember"]:
        return db.session.query(cls).filter(cls.league_id == league_id).all()

    @classmethod
    def find_all_by_user_id(cls, user_id: int) -> List["LeagueMember"]:
        return db.session.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def find_limit_all_enabled_by_user_id(cls, user_id: int, count: int) -> List["LeagueMember"]:
        return db.session.query(cls).\
            filter(cls.user_id == user_id, cls.enabled).\
            order_by(sa.desc(cls.updated_at)).\
            limit(count).\
            all()

    @classmethod
    def find_or_initialize_by_league_id_and_user_id(
        cls, league_id: int, user_id: int
    ) -> "LeagueMember":
        league_member = LeagueMember()
        league_member.league_id = league_id
        league_member.user_id = user_id
        return (
            db.session.query(cls)
            .filter(cls.league_id == league_id, cls.user_id == user_id)
            .one_or_none()
            or league_member
        )
