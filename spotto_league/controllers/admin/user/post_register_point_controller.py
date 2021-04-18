import asyncio
import json
from typing import Dict, Any, List
from collections import defaultdict
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, redirect, url_for
from flask_login import current_user
from spotto_league.models.user import User
from spotto_league.models.bonus_point import BonusPoint
from spotto_league.models.user_point import UserPoint


class PostRegisterPointController(BaseController):
    __slots__ = ['_bonus_points']

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        if not self.login_user.is_admin():
            raise Exception("User: {} is not admin.".format(current_user.login_name))

        self._bonus_points = BonusPoint.all()

        exception = Exception("マイナスの値を入力することはできません。")
        base_point = int(request.form.get("base") or 0)
        if base_point < 0:
            raise exception
        for i in range(8):
            point = int(request.form.get("league_{}".format(i)) or 0)
            if point < 0:
                raise exception

        login_name = request.form.get("user-select")
        user = User.find_by_login_name(login_name)
        for bp in self._bonus_points:
            count = int(request.form.get("bonus_{}".format(bp.id)) or 0)
            if count < 0:
                raise exception
            if bp.user_id == user.id:
                raise Exception("ボーナスポイントは自分自身に付与できません。")

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        memo = "created by {}".format(self.login_user.login_name)
        login_name = request.form.get("user-select")
        base_point = int(request.form.get("base") or 0)
        user = User.find_by_login_name(login_name)
        if base_point > 0:
            user_point = UserPoint()
            user_point.user_id = user.id
            user_point.set_point(int(request.form.get("base") or 0), 'BasePoint', memo)
            user_point.save()

        for i in range(8):
            point = int(request.form.get("league_{}".format(i)) or 0)
            if point > 0:
                up = UserPoint()
                up.user_id = user.id
                up.set_point(point, 'LeaguePoint', memo)
                up.save()

        for bp in self._bonus_points:
            count = int(request.form.get("bonus_{}".format(bp.id)) or 0)
            if count == 0:
                continue
            for i in range(count):
                up = UserPoint()
                up.user_id = user.id
                up.set_bonus_point(bp)
                up.memo = memo
                up.save()

        return redirect(url_for('user_info', login_name=user.login_name), code=307)
