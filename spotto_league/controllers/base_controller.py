from abc import ABCMeta, abstractmethod
import asyncio
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask.wrappers import Request as FlaskRequest
from typing import Dict, Any

class BaseController(metaclass=ABCMeta):
    @abstractmethod
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    @abstractmethod
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        pass

    @asyncio.coroutine
    def get_json(self, request: BaseRequest, **kwargs) -> Dict[str, Any]:
        return {}

    def render(self, request: BaseRequest, **kwargs) -> BaseResponse:
        @asyncio.coroutine
        def _render():
            self.validate(request, **kwargs)
            layout = self.get_layout(request, **kwargs)
            return layout
        return asyncio.get_event_loop().run_until_complete(_render())

    def render_as_json(self, request: BaseRequest, **kwargs) -> Dict[str, Any]:
        @asyncio.coroutine
        def _render():
            self.validate(request, **kwargs)
            layout = self.get_json(request, **kwargs)
            return layout
        return asyncio.get_event_loop().run_until_complete(_render())
