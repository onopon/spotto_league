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
        user_join_league_ids = [m.league_id for m in LeagueMember.find_all_by_user_id(self.login_user.id)]
        for league in league_list:
            if league.is_recruiting():
                league_list_hash['recruiting'].append(league)
            elif league.is_in_session():
                league_list_hash['in_session'].append(league)
            elif league.is_after_session():
                league_list_hash['affter_session'].append(league)
            elif league.is_stopped_recruiting():
                league_list_hash['stopped_recruiting'].append(league)
        return self.render_template("league_list.html",
                                    user_join_league_ids=user_join_league_ids,
                                    league_list_hash=league_list_hash)
