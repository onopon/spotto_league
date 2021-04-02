import asyncio
from .base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_member import User
from collections import defaultdict


class LeagueListController(BaseController):
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        league_list = League.all()
        league_list_hash = defaultdict(list)
        league_members = LeagueMember.find_all_by_user_id(self.login_user.id)
        user_join_league_ids = []
        user_join_enable_league_ids = []
        user_join_disable_league_ids = []
        for lm in league_members:
            user_join_league_ids.append(lm.league_id)
            if lm.enabled:
                user_join_enable_league_ids.append(lm.league_id)
            else:
                user_join_disable_league_ids.append(lm.league_id)
        for league in league_list:
            if league.is_on_today():
                league_list_hash['today'].append(league)
            elif league.is_status_recruiting():
                league_list_hash['status_recruiting'].append(league)
            elif league.is_status_ready():
                if league.is_after_session():
                    league_list_hash['status_finished'].append(league)
                else:
                    league_list_hash['status_ready'].append(league)
            elif league.is_status_finished():
                league_list_hash['status_finished'].append(league)
        return self.render_template("league_list.html",
                                    user_join_league_ids=user_join_league_ids,
                                    user_join_enable_league_ids=user_join_enable_league_ids,
                                    user_join_disable_league_ids=user_join_disable_league_ids,
                                    league_list_hash=league_list_hash)
