import asyncio
import json
from typing import Dict, Any, List
from collections import defaultdict
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template
from flask_login import current_user
from spotto_league.models.user import User
from spotto_league.models.role import RoleType
from spotto_league.models.bonus_point import BonusPoint


class ListController(BaseController):
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        if not self.login_user.is_admin():
            raise Exception("User: {} is not admin.".format(current_user.login_name))

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        users = User.all()
        role_type_hash_list = RoleType.all()
        return self.render_template("admin/user/list.html",
                                    users=users,
                                    role_type_hash_list=role_type_hash_list)
