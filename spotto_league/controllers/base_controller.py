from abc import ABCMeta, abstractmethod
import json
import asyncio
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask.wrappers import Request as FlaskRequest
from typing import Dict, Any
import time
from flask import render_template
from flask_login import current_user
from spotto_league.models.user import User


class BaseController(metaclass=ABCMeta):
    __slots__ = ['login_user']

    def __init__(self):
        if current_user.is_authenticated:
            self.login_user = User.find_by_login_name(current_user.login_name)

    @abstractmethod
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    @asyncio.coroutine
    def get_layout_as_exception(self, request: BaseRequest, error: Exception, **kwargs) -> None:
        return self.render_template("error.html", error_message=str(error))

    @abstractmethod
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        pass

    @asyncio.coroutine
    def get_json(self, request: BaseRequest, **kwargs) -> Dict[str, Any]:
        return {}

    def render(self, request: BaseRequest, **kwargs) -> BaseResponse:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.validate(request, **kwargs))
        except Exception as e:
            return loop.run_until_complete(self.get_layout_as_exception(request, e, **kwargs))
        return loop.run_until_complete(self.get_layout(request, **kwargs))

    def render_as_json(self, request: BaseRequest, **kwargs) -> Dict[str, Any]:
        @asyncio.coroutine
        def _render():
            self.validate(request, **kwargs)
            layout = self.get_json(request, **kwargs)
            return layout
        return asyncio.get_event_loop().run_until_complete(_render())

    def render_template(self, template_name_or_list, **context):
        context['timestamp'] = time.time()
        if current_user.is_authenticated:
            context['login_user'] = self.login_user
        return render_template(template_name_or_list, **context)
