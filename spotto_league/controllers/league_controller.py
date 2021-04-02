import asyncio
import json
from typing import Dict, Any, List
from collections import defaultdict
from .base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template
from flask_login import current_user
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail
from spotto_league.entities.rank import Rank
from spotto_league.entities.point_rank import PointRank
from spotto_league.database import db


class LeagueController(BaseController):
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        # あとでleague_id がNotFoundだった時のエラーを書く
        pass

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        league_id = kwargs["league_id"]
        league = db.session.query(League).get(league_id)
        user_hash, league_log_hash = self._get_user_hash_and_league_log_hash(league_id)
        ranks = Rank.make_rank_list(league)
        rank_user_ids = [r.user_id for r in ranks]
        rank_hash = dict(zip(rank_user_ids, [r.to_hash() for r in ranks]))

        params = {}
        params['league'] = league
        params['is_join'] = current_user.login_name in [u.login_name for u in user_hash.values()]
        params['users'] = list(user_hash.values())
        params['league_log_hash'] = league_log_hash
        params['rank_user_ids'] = rank_user_ids
        params['rank_hash'] = rank_hash

        if league.is_status_finished():
            params['point_ranks'] = PointRank.make_point_rank_list(league)

        return self.render_template("league.html",
                **params)

    # override
    @asyncio.coroutine
    def get_json(self, request: BaseRequest, **kwargs) -> Dict[str, Any]:
        league_id = kwargs["league_id"]
        league = db.session.query(League).get(league_id)
        _, league_log_hash = self._get_user_hash_and_league_log_hash(league_id)
        ranks = Rank.make_rank_list(league)
        rank_user_ids = [r.user_id for r in ranks]
        rank_hash = dict(zip(rank_user_ids, [r.to_hash() for r in ranks]))
        return json.dumps({'game_count': league.game_count,
                           'league_log_hash': league_log_hash,
                           'rank_hash': rank_hash})

    def _get_user_hash_and_league_log_hash(self, league_id):
        league_members = db.session.query(LeagueMember).\
            filter_by(league_id=league_id, enabled=True).all()
        users_hash = {}
        for league_member in league_members:
            user = league_member.user
            users_hash[user.id] = user

        league_log_hash = {}
        for user in users_hash.values():
            for user_2 in users_hash.values():
                if (user.id == user_2.id):
                    continue
                league_log_hash["{}-{}".format(user.id, user_2.id)] =\
                        {'user_id_1': user.id,
                         'user_id_2': user_2.id,
                         'user_name_1': user.name,
                         'user_name_2': user_2.name,
                         'count_1': 0,
                         'count_2': 0,
                         'details_hash_list': []
                         }
        league_logs = db.session.query(LeagueLog).filter_by(league_id=league_id).all()
        for log in league_logs:
            details = log.details
            count_1 = [d.score_1 > d.score_2 for d in details].count(True)
            count_2 = [d.score_1 < d.score_2 for d in details].count(True)
            details_hash_list = [{'score_1': d.score_1, 'score_2': d.score_2} for d in details]
            league_log_hash["{}-{}".format(log.user_id_1, log.user_id_2)]['count_1'] = count_1
            league_log_hash["{}-{}".format(log.user_id_1, log.user_id_2)]['count_2'] = count_2
            league_log_hash["{}-{}".format(log.user_id_1, log.user_id_2)]['details_hash_list'] = details_hash_list

            reverse_details_hash_list = [{'score_1': d.score_2, 'score_2': d.score_1} for d in details]
            league_log_hash["{}-{}".format(log.user_id_2, log.user_id_1)]['count_1'] = count_2
            league_log_hash["{}-{}".format(log.user_id_2, log.user_id_1)]['count_2'] = count_1
            league_log_hash["{}-{}".format(log.user_id_2, log.user_id_1)]['details_hash_list'] = reverse_details_hash_list
        return [users_hash, league_log_hash]
