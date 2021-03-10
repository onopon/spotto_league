from datetime import datetime
from spotto_league.database import db
from typing import Dict, Any
from spotto_league.database import SpottoDB
from spotto_league.models.user import User


class LeagueMember(db.Model):

    __tablename__ = 'league_members'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @property
    def user(self) -> User:
        return SpottoDB().session.query(User).\
            filter_by(id = self.user_id).one()
