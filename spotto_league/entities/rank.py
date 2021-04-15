from typing import List, Dict, Any
from itertools import groupby
from spotto_league.models.user import User
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail
from spotto_league.modules.league_settlement_calculator import LeagueSettlementCalculator


class Rank():
    __slots__ = ['_league_member',
                 '_user_id',
                 '_logs',
                 '_details',
                 '_win_user_ids',
                 '_lose_user_ids',
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
        self._league_member = league_member
        self._user_id = league_member.user_id
        self._logs = logs
        self._details = details
        self._win_user_ids = []
        self._lose_user_ids = []
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
                    self._win_user_ids.append(log.user_id_2)
                else:
                    self._lose_user_ids.append(log.user_id_2)
            else:
                self._got_game += count_2
                self._lost_game += count_1
                self._got_point += sum([d.score_2 for d in details])
                self._lost_point += sum([d.score_1 for d in details])
                if count_1 > count_2:
                    self._lose_user_ids.append(log.user_id_1)
                else:
                    self._win_user_ids.append(log.user_id_1)

    def set_rank(self, rank: int) -> None:
        self._rank = rank

    def set_reason_for_priority(self, reason_of_prioritiy: str) -> None:
        reason = '単独'
        if (reason_of_prioritiy == 'game_of_difference'):
            reason = "ゲーム数による得失点差: {}".format(self.game_of_difference)
        elif (reason_of_prioritiy == 'point_of_difference'):
            reason = "獲得ポイント数による得失点差: {}".format(self.point_of_difference)
        elif (reason_of_prioritiy == 'league_member_id'):
            reason = "参加表明時刻の差: {}".format(self.league_member.created_at)
        self._reason = reason

    def set_reason(self, reason: str) -> None:
        self._reason = reason

    @property
    def league_member(self) -> LeagueMember:
        return self._league_member

    @property
    def league_member_id(self) -> int:
        return self._league_member.id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def win(self) -> int:
        return len(self._win_user_ids)

    @property
    def lose(self) -> int:
        return len(self._lose_user_ids)

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
        if self.win + self.lose == 0:
            return 0.0
        return round(self.win / (self.win + self.lose), 4)

    @property
    def game_of_difference(self) -> int:
        return self._got_game - self._lost_game

    @property
    def point_of_difference(self) -> int:
        return self._got_point - self._lost_point

    def did_win(self, user_id:int) -> bool:
        return user_id in self._win_user_ids

    def to_hash(self) -> Dict[str, Any]:
        return {'rank': self.rank,
                'user_name': self.user.name,
                'login_name': self.user.login_name,
                'win': self.win,
                'lose': self.lose,
                'reason': self._reason}

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
            rank.set_rank(i+1)
        return sorted_rank_list

    @classmethod
    def sort_rank_list(cls, rank_list: List['Rank'], grouping_point: str, count: int = 0) -> List['Rank']:
        sorted_rank_list = []
        for _, group in groupby(rank_list, key=lambda r: getattr(r, grouping_point)):
            ranks = list(group)
            # 単独で順位が確定してる場合
            if len(ranks) == 1:
                [r.set_reason_for_priority(grouping_point) for r in ranks]
                sorted_rank_list.extend(ranks)
                continue
            # ポイントが並んでいる選手が2人いる場合
            elif len(ranks) == 2:
                (rank_1, rank_2) = ranks
                logs = [l for l in rank_1.logs if l.is_in_user_id(rank_2.user_id)]
                # 直接対決があった場合は勝った方の順位を優先
                if len(logs) > 0:
                    details = [d for d in logs[0].details if d.league_log_id == logs[0].id]
                    win_user_id = LeagueSettlementCalculator.get_win_of_head_to_head_user_id(logs[0], details)
                    if rank_1.user_id == win_user_id:
                        rank_1.set_reason("{} と {} の直接対決".format(rank_1.user.name, rank_2.user.name))
                        rank_2.set_reason("{} と {} の直接対決".format(rank_1.user.name, rank_2.user.name))
                        sorted_rank_list.extend([rank_1, rank_2])
                    else:
                        rank_2.set_reason("{} と {} の直接対決".format(rank_2.user.name, rank_1.user.name))
                        rank_1.set_reason("{} と {} の直接対決".format(rank_2.user.name, rank_1.user.name))
                        sorted_rank_list.extend([rank_2, rank_1])
                    continue
            # 直接対決がない or 3つ巴以上が起きている場合
            sort_priorities = ['game_of_difference', 'point_of_difference', 'league_member_id']
            sort_priority = sort_priorities[count]
            ranks.sort(key=lambda r: getattr(r, sort_priority), reverse=True)
            sorted_rank_list.extend(cls.sort_rank_list(ranks, sort_priority, count+1))
        return sorted_rank_list
