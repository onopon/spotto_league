from abc import ABCMeta, abstractmethod
import asyncio
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask.wrappers import Request as FlaskRequest

class BaseController(metaclass=ABCMeta):
    __slots__ = ['session']
    def __init__(self, session):
        self.session = session

    @abstractmethod
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    @abstractmethod
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        pass

    def render(self, request: BaseRequest, **kwargs) -> BaseResponse:
        @asyncio.coroutine
        def _render():
            self.validate(request, **kwargs)
            layout = self.get_layout(request, **kwargs)
            return layout
        return asyncio.get_event_loop().run_until_complete(_render())
