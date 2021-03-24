from typing import List
from itertools import groupby
from spotto_league.models.user import User
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail
from spotto_league.modules.league_settlement_calculator import LeagueSettlementCalculator


class Rank():
    __slots__ = ['_league_member_id',
                 '_user_id',
                 '_logs',
                 '_details',
                 '_win',
                 '_lose',
                 '_got_game',
                 '_lost_game',
                 '_got_point',
                 '_lost_point',
                 '_rank',
                 '_reason']

    def __init__(self,
                 league_member: LeagueMember,
                 logs: List[LeagueLog],
                 details: List[LeagueLogDetail]):
        self._league_member_id = league_member.id
        self._user_id = league_member.user_id
        self._logs = logs
        self._details = details
        self._win = 0
        self._lose = 0
        self._got_game = 0
        self._lost_game = 0
        self._got_point = 0
        self._lost_point = 0
        self.calcurate_points()

    def calcurate_points(self) -> None:
        for log in self._logs:
            details = [d for d in self._details if d.league_log_id == log.id]
            count_1 = [d.score_1 > d.score_2 for d in details].count(True)
            count_2 = [d.score_1 < d.score_2 for d in details].count(True)
            if log.user_id_1 == self._user_id:
                self._got_game += count_1
                self._lost_game += count_2
                self._got_point += sum([d.score_1 for d in details])
                self._lost_point += sum([d.score_2 for d in details])
                if count_1 > count_2:
                    self._win += 1
                else:
                    self._lose += 1
            else:
                self._got_game += count_2
                self._lost_game += count_1
                self._got_point += sum([d.score_2 for d in details])
                self._lost_point += sum([d.score_1 for d in details])
                if count_1 > count_2:
                    self._lose += 1
                else:
                    self._win += 1

    def set_rank_and_reason(self, rank: int, reason: str = "") -> None:
        self._rank = rank
        self._reason = reason

    @property
    def league_member_id(self) -> int:
        return self._league_member_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def win(self) -> int:
        return self._win

    @property
    def lose(self) -> int:
        return self._lose

    @property
    def logs(self) -> List[LeagueLog]:
        return self._logs

    @property
    def details(self) -> List[LeagueLogDetail]:
        return self._details

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def user(self) -> User:
        return User.find(self._user_id)

    @property
    def win_point(self) -> float:
        return round(self.win / (self._win + self._lose), 4)

    @property
    def game_of_difference(self) -> int:
        return self._got_game - self._lost_game

    @property
    def point_of_difference(self) -> int:
        return self._got_point - self._lost_point

    @classmethod
    def make_rank_list(cls, league: League) -> List['Rank']:
        members = league.enable_members
        logs = league.logs
        settlement_hash = LeagueSettlementCalculator.get_settlement_hash(members, logs)
        rank_list = []
        for member in members:
            settlement = settlement_hash[member.user_id]
            rank = Rank(member,
                        settlement['logs'],
                        settlement['details'])
            rank_list.append(rank)
        rank_list.sort(key=lambda r: r.win_point, reverse=True)
        sorted_rank_list = cls.sort_rank_list(rank_list, 'win_point')
        for i, rank in enumerate(sorted_rank_list):
            rank.set_rank_and_reason(i+1)
        return sorted_rank_list

    @classmethod
    def sort_rank_list(cls, rank_list: List['Rank'], grouping_point: str, count: int = 0) -> List['Rank']:
        sorted_rank_list = []
        for _, group in groupby(rank_list, key=lambda r: getattr(r, grouping_point)):
            ranks = list(group)
            # 単独で順位が確定してる場合
            if len(ranks) == 1:
                sorted_rank_list.extend(ranks)
                continue
            # ポイントが並んでいる選手が2人いる場合
            elif len(ranks) == 2:
                (rank_1, rank_2) = ranks
                logs = [l for l in logrank_1.logs if l.is_in_user_id(rank_2.user_id)]
                # 直接対決があった場合は勝った方の順位を優先
                if len(logs) > 0:
                    details = [d for d in self.details if d.league_log_id == logs[0].id]
                    win_user_id = LeagueSettlementCalculator.get_win_of_head_to_head_user_id(log[0], details)
                    if rank_1.user_id == win_user_id:
                        sorted_rank_list.extend([rank_1, rank_2])
                    else:
                        sorted_rank_list.extend([rank_2, rank_1])
                    continue
            # 直接対決がない or 3つ巴以上が起きている場合
            sort_priorities = ['game_of_difference', 'point_of_difference', 'league_member_id']
            sort_priority = sort_priorities[count]
            ranks.sort(key=lambda r: getattr(r, sort_priority))
            sorted_rank_list.extend(cls.sort_rank_list(ranks, sort_priority, count+1))
        return sorted_rank_list
