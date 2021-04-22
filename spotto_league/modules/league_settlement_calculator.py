from typing import Any, List
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail
from collections import defaultdict


class LeagueSettlementCalculator():
    @classmethod
    def get_settlement_hash(cls, members: List[LeagueMember], logs: List[LeagueLog]):
        settlement_hash = defaultdict(lambda: dict())
        count_of_games = len(members) - 1  # 初期値は出来うる試合数の最大値としておく
        # ここで選手ごとにlogを分ける
        for member in members:
            member_logs = [l for l in logs if l.is_in_user_id(member.user_id)]
#            if count_of_games > len(member_logs):
#                count_of_games = len(member_logs)
            settlement_hash[member.user_id]['logs'] = member_logs

        for member in members:
            member_logs = settlement_hash[member.user_id]['logs'][:count_of_games]
            settlement_hash[member.user_id]['logs'] = member_logs
            settlement_hash[member.user_id]['details'] = LeagueLogDetail.find_all_by_league_log_ids([l.id for l in member_logs])
        return settlement_hash
        
    @classmethod
    def get_win_of_head_to_head_user_id(cls, log, details) -> int:
        count_1 = [d.score_1 > d.score_2 for d in details].count(True)
        count_2 = [d.score_1 < d.score_2 for d in details].count(True)
        return log.user_id_1 if count_1 > count_2 else log.user_id_2
