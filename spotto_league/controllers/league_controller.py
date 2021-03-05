
import asyncio
from collections import defaultdict
from .base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template
from spotto_league.models.league import League
from spotto_league.models.user import User
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail


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
        league = self.session.query(League).get(league_id)
        league_members_and_users = self.session.query(LeagueMember, User).\
            filter_by(league_id=league_id, enabled=True).\
            join(LeagueMember, User.id==LeagueMember.user_id).\
            all()

        league_log_hash = {}
        league_logs = self.session.query(LeagueLog).filter_by(league_id=league_id).all()
        for log in league_logs:
            league_log_hash[log.user_id_1, log.user_id_2] = log

        league_log_details = self.session.query(LeagueLogDetail).\
            filter(LeagueLogDetail.league_log_id.in_([log.id for log in league_logs])).all()

        league_log_detail_hash = defaultdict(list)
        for detail in league_log_details:
            league_log_detail_hash[detail.league_log_id].append(detail)

        game_count_hash = {}
        for league_log_id, details in league_log_detail_hash.items():
            left_count = [d.score_1 > d.score_2 for d in details].count(True)
            right_count = [d.score_1 < d.score_2 for d in details].count(True)
            game_count_hash[league_log_id]  = (left_count, right_count)

        return render_template("league.html",
                league=league,
                league_members_and_users=league_members_and_users,
                league_log_hash=league_log_hash,
                league_log_detail_hash=league_log_detail_hash,
                game_count_hash=game_count_hash)
