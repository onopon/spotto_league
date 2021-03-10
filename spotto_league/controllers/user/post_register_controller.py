import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template
from spotto_league.models.user import User
from spotto_league.database import SpottoDB


class PostRegisterController(BaseController):
    # override
    def validate(self, request: BaseRequest, **kwargs) -> None:
        # TODO: 後でやる
        login_name = request.form.get("login_name")
        name = request.form.get("name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if (password != confirm_password):
            raise Exception()

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        login_name = request.form.get("login_name")
        name = request.form.get("name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        user = User()
        user.login_name = login_name
        user.name = name
        user.set_password(password)
        user.save()
        return render_template("user/register_complete.html", login_name=user.login_name, name=user.name)
