from typing import List
from spotto_league.database import SpottoDB, db
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.place import Place
from spotto_league.models.league_member import LeagueMember
from .base import Base
import datetime
from datetime import datetime as dt
from enum import Enum


class LeagueStatus(Enum):
    RECRUITING = 0
    READY = 1
    FINISHED = 2


class League(db.Model, Base):

    __tablename__ = 'leagues'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=dt.now().date, index=True)
    name = db.Column(db.String(255), nullable=False)
    game_count = db.Column(db.Integer, nullable=False, index=True)
    start_at = db.Column(db.Time, nullable=False, default=dt.now().time)
    end_at = db.Column(db.Time, nullable=False, default=dt.now().time)
    join_end_at = db.Column(db.DateTime, nullable=False, default=dt.now)
    status = db.Column(db.Integer, nullable=False, default=False, index=True)
    place_id = db.Column(db.Integer, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=dt.now, onupdate=dt.now)

    @property
    def place(self) -> Place:
        return Place.find(self.place_id)

    @property
    def members(self) -> List[LeagueMember]:
        return LeagueMember.find_all_by_league_id(self.id)

    @property
    def logs(self) -> List[LeagueLog]:
        return self.session.query(LeagueLog).\
                filter_by(league_id=self.id).all()

    def ready(self) -> None:
        self.status = LeagueStatus.READY.value

    def finish(self) -> None:
        self.status = LeagueStatus.FINISHED.value

    def is_status_recruiting(self) -> bool:
        return LeagueStatus(self.status) == LeagueStatus.RECRUITING

    def is_status_ready(self) -> bool:
        return LeagueStatus(self.status) == LeagueStatus.READY

    def is_status_finished(self) -> bool:
        return LeagueStatus(self.status) == LeagueStatus.FINISHED

    @classmethod
    def all(cls) -> List['League']:
        return db.session.query(League).all()

    @classmethod
    def all_yet_recruiting(cls) -> List['League']:
        return db.session.query(cls).filter(cls.end_at > dt.now(), cls.status == 0)


    def is_recruiting(self) -> bool:
        return self.is_status_recruiting() and dt.now() < self.join_end_at

    def is_stopped_recruiting(self) -> bool:
        return self.is_status_ready() or dt.now() > self.join_end_at

    # TODO: is_ready() だけど時間外になってる状態のleagueデータを考える
    def is_in_session(self) -> bool:
        now = dt.now()
        return self.is_status_ready() and\
                dt.combine(self.date, self.start_at) < now and\
                now < dt.combine(self.date, self.end_at)

    def is_after_session(self) -> bool:
        return self.is_status_finished() and (dt.combine(self.date, self.end_at) < dt.now())
