from typing import List
from spotto_league.database import db
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.place import Place
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_point import LeaguePoint
from .base import Base
from datetime import datetime as dt
from datetime import date
from enum import Enum
from sqlalchemy import and_


NEAR_JOIN_END_AT_SECONDS = 3 * 60 * 60  # 参加締め切り時刻に近いとする時間（秒）


class LeagueStatus(Enum):
    RECRUITING = 0
    READY = 1
    FINISHED = 2
    RECRUITING_NEAR_JOIN_END_AT = 3
    CANCEL = 4


class League(db.Model, Base):

    __tablename__ = "leagues"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=dt.now().date, index=True)
    name = db.Column(db.String(255), nullable=False)
    game_count = db.Column(db.Integer, nullable=False, index=True)
    start_at = db.Column(db.Time, nullable=False, default=dt.now().time)
    end_at = db.Column(db.Time, nullable=False, default=dt.now().time)
    join_end_at = db.Column(db.DateTime, nullable=False, default=dt.now)
    status = db.Column(db.Integer, nullable=False, default=False, index=True)
    place_id = db.Column(db.Integer, nullable=False, index=True)
    league_point_group_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: dt.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: dt.now(), onupdate=lambda: dt.now())
    _place = None
    _members = None
    _logs = None
    _league_points = None

    @property
    def place(self) -> Place:
        if not self._place:
            self._place = Place.find(self.place_id)
        return self._place

    @property
    def members(self) -> List[LeagueMember]:
        if not self._members:
            self._members = LeagueMember.find_all_by_league_id(self.id)
        return self._members

    @property
    def enable_members(self) -> List[LeagueMember]:
        return [m for m in self.members if m.enabled]

    @property
    def logs(self) -> List[LeagueLog]:
        if not self._logs:
            self._logs = LeagueLog.find_all_by_league_id(self.id)
        return self._logs

    @property
    def recommend_league_point_group_id(self) -> int:
        member_count = len(self.members)
        if member_count < LeaguePoint.RATING_BORDER_MEMBER_COUNT:
            return LeaguePoint.BASE_GROUP_ID
        return LeaguePoint.ONE_AND_HALF_TIMES_GROUP_ID

    @property
    def league_points(self) -> List[LeaguePoint]:
        if self.league_point_group_id is None:
            return []
        if not self._league_points:
            self._league_points = LeaguePoint.find_all_by_group_id(
                self.league_point_group_id
            )
        return self._league_points

    @property
    def date_for_display(self) -> str:
        w_list = ["月", "火", "水", "木", "金", "土", "日"]
        date_str = self.date.strftime("%m月%d日")
        start_at_str = "{}:{}".format(
            str(self.start_at.hour).zfill(2), str(self.start_at.minute).zfill(2)
        )
        end_at_str = "{}:{}".format(
            str(self.end_at.hour).zfill(2), str(self.end_at.minute).zfill(2)
        )
        return "{}（{}）{} - {}".format(
            date_str, w_list[self.date.weekday()], start_at_str, end_at_str
        )

    @property
    def time_for_display(self) -> str:
        start_at_str = "{}:{}".format(
            str(self.start_at.hour).zfill(2), str(self.start_at.minute).zfill(2)
        )
        end_at_str = "{}:{}".format(
            str(self.end_at.hour).zfill(2), str(self.end_at.minute).zfill(2)
        )
        return "{} - {}".format(start_at_str, end_at_str)

    @property
    def join_end_at_for_display(self) -> str:
        return self.join_end_at.strftime("%m月%d日（%a）%H:%M")

    @property
    def start_datetime(self) -> dt:
        return dt.combine(self.date, self.start_at)

    def league_point_group_id_is(self, group_id: int) -> bool:
        return group_id == self.recommend_league_point_group_id

    def recruiting_near_join_end_at(self) -> None:
        self.status = LeagueStatus.RECRUITING_NEAR_JOIN_END_AT.value

    def ready(self) -> None:
        self.status = LeagueStatus.READY.value

    def finish(self) -> None:
        self.status = LeagueStatus.FINISHED.value

    def cancel(self) -> None:
        self.status = LeagueStatus.CANCEL.value

    def is_on_today(self) -> bool:
        return self.date == dt.now().date()

    def is_status_recruiting(self) -> bool:
        return (
            LeagueStatus(self.status) == LeagueStatus.RECRUITING
            or self.is_status_recruiting_near_join_end_at()
        )

    def is_status_recruiting_near_join_end_at(self) -> bool:
        return LeagueStatus(self.status) == LeagueStatus.RECRUITING_NEAR_JOIN_END_AT

    def is_status_ready(self) -> bool:
        return LeagueStatus(self.status) == LeagueStatus.READY

    def is_status_finished(self) -> bool:
        return (
            LeagueStatus(self.status) == LeagueStatus.FINISHED
            or self.is_status_cancel()
        )

    def is_status_cancel(self) -> bool:
        return LeagueStatus(self.status) == LeagueStatus.CANCEL

    @classmethod
    def all(cls) -> List["League"]:
        return db.session.query(League).all()

    @classmethod
    def find_all_for_cosecutive_win_bonus_point(cls) -> List["League"]:
        year = dt.today().year
        # 2021/8/18 より適用開始
        target_date = date(year, 8, 18) if year == 2021 else date(year, 1, 1)
        items = db.session.query(cls).\
            filter(and_(cls.status == LeagueStatus.FINISHED.value,
                        cls.league_point_group_id != 0,
                        cls.date >= target_date)).\
            all()
        return sorted(
            items,
            key=lambda x: (x.date, x.end_at),
            reverse=True
        )

    def is_in_join_session(self) -> bool:
        return dt.now() < self.join_end_at

    def is_stopped_recruiting(self) -> bool:
        return self.is_status_ready() or dt.now() > self.join_end_at

    def is_before_session(self) -> bool:
        return dt.now() < dt.combine(self.date, self.start_at)

    def is_in_session(self) -> bool:
        now = dt.now()
        return dt.combine(self.date, self.start_at) <= now and now <= dt.combine(
            self.date, self.end_at
        )

    def is_after_session(self) -> bool:
        return dt.combine(self.date, self.end_at) < dt.now()

    def is_near_join_end_at(self) -> bool:
        if not self.is_status_recruiting():
            return False

        now = dt.now()
        if self.join_end_at < now:
            return False

        delta = self.join_end_at - now
        if delta.days > 0:
            return False
        return delta.seconds <= NEAR_JOIN_END_AT_SECONDS
