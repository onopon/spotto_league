import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template, redirect, url_for
from spotto_league.models.user import User
from spotto_league.modules.password_util import PasswordUtil
import flask_login


class PostLoginController(BaseController):
    __slots__ = ['_user']
    # override
    def validate(self, request: BaseRequest, **kwargs) -> None:
        login_name = request.form.get("login_name")
        password = request.form.get("password")
        user = User.find_by_login_name(self.session, login_name)
        if not user:
            raise Exception()
        if not PasswordUtil.is_same(password, user.password):
            raise Exception()
        self._user = user

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        user = User()
        user.id = self._user.login_name
        user.login_name = self._user.login_name
        flask_login.login_user(user)
        return redirect(url_for('league_list'))
