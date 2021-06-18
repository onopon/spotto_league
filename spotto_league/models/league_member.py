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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    _user = None

    @property
    def user(self) -> User:
        if not self._user:
            self._user = User.find(self.user_id)
        return self._user

    @classmethod
    def find_all_by_league_id(cls, league_id) -> List["LeagueMember"]:
        return db.session.query(cls).filter(cls.league_id == league_id).all()

    @classmethod
    def find_all_by_user_id(cls, user_id) -> List["LeagueMember"]:
        return db.session.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def find_or_initialize_by_league_id_and_user_id(
        cls, league_id, user_id
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
