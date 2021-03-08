import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template, redirect
from flask_login import current_user
import flask_login


class LoginController(BaseController):
    # override
    def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        flask_login.logout_user()
        if current_user.is_authenticated:
            return redirect(flask.url_for('/'))
        return render_template("user/login.html")
