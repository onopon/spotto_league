import asyncio
import json
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template, redirect, url_for
from spotto_league.models.league import League
from spotto_league.models.user import User
from spotto_league.models.league_member import LeagueMember
import flask_login


class PostLeagueJoinController(BaseController):
    # override
    def enable_for_visitor(self) -> bool:
        return True

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        league_id = request.form.get("league_id")
        try:
            League.find(league_id)
        except:
            raise Exception("League: {} does not exist.".format(league_id))

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        league_id = request.form.get("league_id")
        user_id = self.login_user.id
        login_name = request.form.get("login_name")
        if login_name:
            user_id = User.find_by_login_name(login_name).id
        league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league_id, user_id)
        if request.form.get("force_join"):
            league_member.enabled = True
        league_member.save()
        return 'success'
