import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, redirect, url_for
from flask_login import current_user
from spotto_league.models.user import User
from spotto_league.models.league import League, LeagueStatus
from spotto_league.entities.point_rank import PointRank
from datetime import date

class PostModifyController(BaseController):
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        if self.login_user.role and not request.form.get("first-name"):
            raise Exception("管理者、チームメンバーのユーザは本名の設定は必須です。")

    @asyncio.coroutine
    def get_layout_as_exception(self, request: BaseRequest, error: Exception, **kwargs) -> None:
        return self.render_template("user/modify.html",
                                    error_message=str(error))

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        self.login_user.name = request.form.get("name")
        self.login_user.first_name = request.form.get("first-name")
        self.login_user.last_name = request.form.get("last-name")
        self.login_user.gender = int(request.form.get("gender"))
        year = int(request.form.get("year"))
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))
        self.login_user.birthday = date(year, month, day)
        self.login_user.save()

        return redirect(url_for('user_info', login_name=self.login_user.login_name))
