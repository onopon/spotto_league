import asyncio
import json
from typing import Dict, Any, List
from collections import defaultdict
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template
from flask_login import current_user
from spotto_league.models.user import User
from spotto_league.models.role import Role, RoleType
from spotto_league.models.bonus_point import BonusPoint

ROLE_TYPE_GUEST = -1


class PostListController(BaseController):
    __slots__  = ['_users']

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        if not self.login_user.is_admin():
            raise Exception("User: {} is not admin.".format(current_user.login_name))

        self._users = User.all()
        for user in self._users:
            role_type_key = "radio_{}".format(user.login_name)
            role_type_value = int(request.form.get(role_type_key))
            if (self.login_user.id == user.id and role_type_value != RoleType.ADMIN.value):
                raise Exception("自分自身を管理者以外に設定することはできません。")
            if ((not user.first_name or not user.last_name) and role_type_value > 0):
                raise Exception("名前の設定がないユーザに役柄を設定することはできません。")

    @asyncio.coroutine
    def get_layout_as_exception(self, request: BaseRequest, error: Exception, **kwargs) -> None:
        role_type_hash_list = RoleType.all()
        return self.render_template("admin/user/list.html",
                                    users=self._users,
                                    role_type_hash_list=role_type_hash_list,
                                    error_message=str(error))

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        role_type_hash_list = RoleType.all()
        for user in self._users:
            role_type_key = "radio_{}".format(user.login_name)
            role_type_value = int(request.form.get(role_type_key))
            if (role_type_value == ROLE_TYPE_GUEST):
                if user.role:
                    user.role.delete()
                continue
            role = user.role or Role()
            role.user_id = user.id
            role.role_type = role_type_value
            role.save()
        return self.render_template("admin/user/list.html",
                                    users=self._users,
                                    role_type_hash_list=role_type_hash_list,
                                    is_success = True)