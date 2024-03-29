from abc import ABCMeta, abstractmethod
import asyncio
from werkzeug.wrappers import BaseRequest, Response
from typing import Dict, Any, Union, Tuple
import time
from flask import render_template, redirect, url_for
from flask_login import current_user, logout_user
from spotto_league.models.user import User
from spotto_league.exceptions import (
    NotAdminException,
    NotMemberException
)

AnyResponse = Union[str, Response, Dict[str, Any], Tuple]


class BaseController(metaclass=ABCMeta):
    __slots__ = ["login_user"]

    def __init__(self):
        if current_user.is_authenticated:
            self.login_user = User.find_by_login_name(current_user.login_name)

    # アクセスする際、ユーザログインを保っているべきであるかどうか
    def should_login(self) -> bool:
        return True

    # アクセスする際、ビジターの人もアクセス可能かどうか
    def enable_for_visitor(self) -> bool:
        return False

    async def validate_for_visitor(self) -> None:
        if self.enable_for_visitor():
            return
        if current_user.is_authenticated and self.login_user.is_visitor():
            raise NotMemberException("ゲストの方はこのページを閲覧することはできません。")

    async def validate_for_withdrawaler(self) -> None:
        if current_user.is_authenticated and self.login_user.is_withdrawaler():
            logout_user()

    @abstractmethod
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    async def get_layout_as_exception(
        self, request: BaseRequest, error: Exception, **kwargs
    ) -> AnyResponse:
        if type(error) in [NotAdminException, NotMemberException]:
            return self.render_template("error.html", 401, error_message=str(error))
        return self.render_template("error.html", 404, error_message=str(error))

    @abstractmethod
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        pass

    async def get_json(self, request: BaseRequest, **kwargs) -> Dict[str, Any]:
        return {}

    def render(self, request: BaseRequest, **kwargs) -> AnyResponse:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.validate_for_visitor())
            loop.run_until_complete(self.validate_for_withdrawaler())
            loop.run_until_complete(self.validate(request, **kwargs))
        except Exception as e:
            return loop.run_until_complete(
                self.get_layout_as_exception(request, e, **kwargs)
            )
        return loop.run_until_complete(self.get_layout(request, **kwargs))

    def render_as_json(self, request: BaseRequest, **kwargs) -> AnyResponse:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.validate_for_visitor())
            loop.run_until_complete(self.validate(request, **kwargs))
        except Exception as e:
            return loop.run_until_complete(
                self.get_layout_as_exception(request, e, **kwargs)
            )
        return loop.run_until_complete(self.get_json(request, **kwargs))

    def render_template(self, template_name_or_list, status_code=200, **context) -> AnyResponse:
        context["timestamp"] = time.time()
        if current_user.is_authenticated:
            context["login_user"] = self.login_user
        else:
            if self.should_login():
                return redirect(url_for("user_login"))

        return render_template(template_name_or_list, **context), status_code
