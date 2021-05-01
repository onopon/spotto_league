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
    def should_login(self) -> bool:
        return False

    # override
    def enable_for_visitor(self) -> bool:
        return True

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        login_name = request.form.get("login_name")
        password = request.form.get("password")
        common_password = request.form.get("common_password")

        # Visitor用validate
        if PasswordUtil.is_correct_common_visitor_password(common_password):
            user = User.find_by_login_name(login_name)
            self._validate(user, password)
            if not user.is_visitor():
                raise Exception("ログイン失敗")
        # それ以外の人用validate
        elif PasswordUtil.is_correct_common_password(common_password):
            user = User.find_by_login_name(login_name)
            self._validate(user, password)
            if user.is_visitor():
                raise Exception("ログイン失敗")
        else:
            raise Exception("ログイン失敗")
        self._user = user

    def _validate(self, user: User, password: str) -> None:
        if not user:
            raise Exception("ログイン失敗")
        if not PasswordUtil.is_same(password, user.password):
            raise Exception("ログイン失敗")

    @asyncio.coroutine
    def get_layout_as_exception(self, request: BaseRequest, error: Exception, **kwargs) -> None:
        return self.render_template("user/login.html", is_miss_login = True)

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        user = User()
        user.id = self._user.login_name
        user.login_name = self._user.login_name
        flask_login.login_user(user)
        return redirect(url_for('league_list'))
