import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template, redirect, url_for
from spotto_league.models.user import User
from datetime import date
import flask_login


class PostRegisterController(BaseController):
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        login_name = request.form.get("login_name")
        name = request.form.get("name")
        gender = int(request.form.get("gender"))
        year = int(request.form.get("year"))
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))
        targets = [login_name, name, gender, str(year), str(month), str(day)]
        if any([len(target) == 0 for target in targets]):
            raise Exception("必要なデータが入力されていません。")


        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if (password != confirm_password):
            raise Exception("パスワードが一致しません。")

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        login_name = request.form.get("login_name")
        name = request.form.get("name")
        password = request.form.get("password")
        gender = int(request.form.get("gender"))
        year = int(request.form.get("year"))
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))
        user = User()
        user.login_name = login_name
        user.name = name
        user.set_password(password)
        user.gender = gender
        user.birthday = date(year, month, day)
        user.save()

        login_user = User()
        login_user.id = user.login_name
        login_user.login_name = user.login_name
        flask_login.login_user(login_user)

        return redirect(url_for('league_list'), code=307)
