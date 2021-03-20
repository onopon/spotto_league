import asyncio
import json
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template, redirect, url_for
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember
import flask_login


class PostLeagueCancelController(BaseController):
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        league_id = request.form.get("league_id")
        try:
            League.find(league_id)
        except:
            raise Exception()

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        league_id = request.form.get("league_id")
        league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league_id, self.login_user.id)
        league_member.delete()
        return 'success'
