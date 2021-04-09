from enum import Enum
from typing import List, Dict, Any
from itertools import groupby
from spotto_league.models.league import League
from spotto_league.models.league_point import LeaguePoint
from spotto_league.models.bonus_point import BonusPoint
from spotto_league.models.user import User
from spotto_league.models.user_point import UserPoint

BASIC_AVAILABLE_COUNT = 8
POINT_HASH_KEY_BONUS = 'BonusPoint'
POINT_HASH_KEY_NORMAL = 'Normal'


class RankSatus(Enum):
    STAY = 1
    DOWN = 2
    UP = 3

class PointRank():
    __slots__ = ['_user',
                 '_before_rank',
                 '_current_rank',
                 '_before_points_hash',
                 '_current_points_hash']

    def __init__(self,
                 user: User,
                 before_points_hash: Dict[str, List[int]],
                 current_points_hash: Dict[str, List[int]]):
        self._user = user
        self._before_points_hash = before_points_hash
        self._current_points_hash = current_points_hash

    @property
    def user(self) -> User:
        return self._user

    @property
    def before_point(self) -> int:
        values = list(self._before_points_hash.values())
        return sum([sum(points) for points in values])

    @property
    def current_point(self) -> int:
        values = list(self._current_points_hash.values())
        return sum([sum(points) for points in values])

    @property
    def before_normal_points(self) -> List[int]:
        return self._before_points_hash[POINT_HASH_KEY_NORMAL]

    @property
    def before_current_points(self) -> List[int]:
        return self._current_points_hash[POINT_HASH_KEY_NORMAL]

    @property
    def before_rank(self) -> int:
        return self._before_rank

    @property
    def current_rank(self) -> int:
        return self._current_rank

    def set_before_rank(self, rank) -> None:
        self._before_rank = rank

    def set_current_rank(self, rank) -> None:
        self._current_rank = rank

    def is_stay(self) -> bool:
        return self._before_rank == self._current_rank

    def is_down(self) -> bool:
        return self._before_rank < self._current_rank

    def is_up(self) -> bool:
        return self._before_rank > self._current_rank

    @classmethod
    def make_point_rank_list_in_season(cls, year: int) -> List['PointRank']:
        user_points = UserPoint.find_all_in_season(year)
        users = User.all()
        bonus_points = BonusPoint.find_all_by_user_ids([u.id for u in users])

        rank_list = []
        for user in users:
            m_user_points = list(filter(lambda up: up.user_id == user.id, user_points))
            current_points = cls.get_sorted_points_hash(m_user_points, bonus_points)
            before_points = {POINT_HASH_KEY_NORMAL: [], POINT_HASH_KEY_BONUS: []}
            rank_list.append(PointRank(user, before_points, current_points))

        current_rank = 1
        sorted_rank_list = []
        rank_list.sort(key=lambda r: r.current_point, reverse=True)
        for _, group in groupby(rank_list, key=lambda r: r.current_point):
            ranks = list(group)
            for rank in ranks:
                rank.set_current_rank(current_rank)
                sorted_rank_list.append(rank)
            current_rank += len(ranks)

        return sorted_rank_list


    @classmethod
    def make_point_rank_list(cls, league: League) -> List['PointRank']:
        user_points = UserPoint.find_all_in_season(league.updated_at.year)
        members = league.enable_members
        users = User.all()

        bonus_points = BonusPoint.find_all_by_user_ids([u.id for u in users])
        rank_list = []
        for user in users:
            m_user_points = list(filter(lambda up: up.user_id == user.id and\
                    up.created_at <= league.updated_at, user_points))
            m_before_points = list(filter(lambda up: up.league_id != league.id and\
                    up.created_at < league.updated_at, m_user_points))
            current_points = cls.get_sorted_points_hash(m_user_points, bonus_points)
            before_points = cls.get_sorted_points_hash(m_before_points, bonus_points)
            rank_list.append(PointRank(user, before_points, current_points))

        before_rank = 1
        sorted_before_rank_list = []
        rank_list.sort(key=lambda r: r.before_point, reverse=True)
        for _, group in groupby(rank_list, key=lambda r: r.before_point):
            ranks = list(group)
            for rank in ranks:
                rank.set_before_rank(before_rank)
                sorted_before_rank_list.append(rank)
            before_rank += len(ranks)

        current_rank = 1
        sorted_rank_list = []
        sorted_before_rank_list.sort(key=lambda r: r.current_point, reverse=True)
        for _, group in groupby(sorted_before_rank_list, key=lambda r: r.current_point):
            ranks = list(group)
            for rank in ranks:
                rank.set_current_rank(current_rank)
                sorted_rank_list.append(rank)
            current_rank += len(ranks)

        return sorted_rank_list

    '''
    全リーグのうち高いポイントをBASIC_AVAILABLE_COUNT分と、ボーナスポイントをavailable_countの分だけ取得
    '''
    @classmethod
    def get_sorted_points_hash(cls, user_points: List[UserPoint], bonus_points: List[BonusPoint]) -> int:
        sorted_points_hash = {POINT_HASH_KEY_NORMAL: [], POINT_HASH_KEY_BONUS: []}
        if len(user_points) == 0:
            return sorted_points_hash
        user_bonus_points = [up for up in user_points if up.reason_class == 'BonusPoint']
        for bp in bonus_points:
            m_bonus_points = [up.point for up in user_bonus_points if up.reason_id == bp.user_id]
            sorted_points_hash[POINT_HASH_KEY_BONUS].extend(m_bonus_points[:bp.available_count])
        sorted_points_hash[POINT_HASH_KEY_BONUS].sort(reverse=True)
        league_point_list = [up.point for up in user_points if up.reason_class != 'BonusPoint']
        league_point_list.sort(reverse=True)
        sorted_points_hash[POINT_HASH_KEY_NORMAL] = league_point_list[:BASIC_AVAILABLE_COUNT]
        return sorted_points_hash
