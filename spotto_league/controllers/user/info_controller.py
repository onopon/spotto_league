import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, redirect, url_for
from flask_login import current_user
from spotto_league.models.user import User
from spotto_league.models.league import League


class InfoController(BaseController):
    __slots__ = ['_user']

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        self._user = User.find_by_login_name(kwargs["login_name"])
        if not self._user:
            raise Exception

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        render_hash = {}
        render_hash['user'] = self._user
        if self._user.id == self.login_user.id:
            if self.login_user.is_admin():
                render_hash['yet_recruiting_league_list'] = League.all_yet_recruiting()
        return self.render_template("user/info.html", **render_hash)
