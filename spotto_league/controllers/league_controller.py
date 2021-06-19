import asyncio
from flask import jsonify
from typing import Dict, Any, List
from .base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from spotto_league.models.league import League
from spotto_league.models.league_log import LeagueLog
from spotto_league.entities.rank import Rank
from spotto_league.entities.point_rank import PointRank


class LeagueController(BaseController):
    __slots__ = ["_league"]

    # override
    def enable_for_visitor(self) -> bool:
        return True

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        league = League.find_by_id(kwargs["league_id"])
        if not league:
            raise Exception("league_id: {} のリーグ戦情報は存在しません。".format(kwargs["league_id"]))
        if self.login_user.is_visitor() and not league.is_on_today():
            raise Exception("ゲストの方はこのページを閲覧することはできません。")
        self._league = league

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        params = {}

        league = self._league
        point_ranks = PointRank.make_point_rank_list(league)
        user_hash, league_log_hash = self._get_user_hash_and_league_log_hash(
            league, point_ranks
        )

        ranks = Rank.make_rank_list(league)
        rank_user_ids = [r.user_id for r in ranks]
        rank_hash = dict(zip(rank_user_ids, [r.to_hash() for r in ranks]))

        params["league"] = league
        params["is_join"] = self.login_user.login_name in [
            u.login_name for u in user_hash.values()
        ]
        params["is_wanted_join"] = self.login_user.id in [
            lm.user_id for lm in league.members
        ]
        params["users"] = list(user_hash.values())
        params["league_log_hash"] = league_log_hash
        params["rank_user_ids"] = rank_user_ids
        params["rank_hash"] = rank_hash
        params["point_ranks"] = point_ranks

        return self.render_template("league.html", **params)

    # override
    @asyncio.coroutine
    def get_json(self, request: BaseRequest, **kwargs) -> Dict[str, Any]:
        league = self._league
        point_ranks = PointRank.make_point_rank_list(league)
        _, league_log_hash = self._get_user_hash_and_league_log_hash(
            league, point_ranks
        )
        ranks = Rank.make_rank_list(league)
        rank_user_ids = [r.user_id for r in ranks]
        rank_hash = dict(zip(rank_user_ids, [r.to_hash() for r in ranks]))
        params = {
            "game_count": league.game_count,
            "league_log_hash": league_log_hash,
            "rank_hash": rank_hash,
            "point_rank_hash": dict(
                zip(
                    [p.user.id for p in point_ranks], [p.to_hash() for p in point_ranks]
                )
            ),
        }
        return jsonify(params)

    def _get_user_hash_and_league_log_hash(
        self, league: League, point_ranks: List[PointRank]
    ):
        league_members = league.enable_members
        user_with_rank_hash = {}
        users_out_of_point_rank = []

        for league_member in league_members:
            for point_rank in point_ranks:
                if league_member.user.id == point_rank.user.id:
                    user_with_rank_hash[point_rank.current_rank] = league_member.user
                    continue
            users_out_of_point_rank.append(league_member.user)

        users_hash = {}
        for rank in sorted(list(user_with_rank_hash.keys())):
            user = user_with_rank_hash[rank]
            users_hash[user.id] = user

        for user in users_out_of_point_rank:
            users_hash[user.id] = user

        league_log_hash = {}
        for user in users_hash.values():
            for user_2 in users_hash.values():
                if user.id == user_2.id:
                    continue
                league_log_hash["{}-{}".format(user.id, user_2.id)] = {
                    "user_id_1": user.id,
                    "user_id_2": user_2.id,
                    "user_name_1": user.name,
                    "user_name_2": user_2.name,
                    "count_1": 0,
                    "count_2": 0,
                    "details_hash_list": [],
                }
        league_logs = LeagueLog.find_all_by_league_id(league.id)
        for log in league_logs:
            details = log.details
            count_1 = [d.score_1 > d.score_2 for d in details].count(True)
            count_2 = [d.score_1 < d.score_2 for d in details].count(True)
            details_hash_list = [
                {"score_1": d.score_1, "score_2": d.score_2} for d in details
            ]
            league_log_hash["{}-{}".format(log.user_id_1, log.user_id_2)][
                "count_1"
            ] = count_1
            league_log_hash["{}-{}".format(log.user_id_1, log.user_id_2)][
                "count_2"
            ] = count_2
            league_log_hash["{}-{}".format(log.user_id_1, log.user_id_2)][
                "details_hash_list"
            ] = details_hash_list

            reverse_details_hash_list = [
                {"score_1": d.score_2, "score_2": d.score_1} for d in details
            ]
            league_log_hash["{}-{}".format(log.user_id_2, log.user_id_1)][
                "count_1"
            ] = count_2
            league_log_hash["{}-{}".format(log.user_id_2, log.user_id_1)][
                "count_2"
            ] = count_1
            league_log_hash["{}-{}".format(log.user_id_2, log.user_id_1)][
                "details_hash_list"
            ] = reverse_details_hash_list
        return [users_hash, league_log_hash]
