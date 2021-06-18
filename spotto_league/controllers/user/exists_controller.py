import asyncio
import json
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from spotto_league.models.user import User


class ExistsController(BaseController):
    # override
    def should_login(self) -> bool:
        return False

    # override
    def enable_for_visitor(self) -> bool:
        return True

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        if not kwargs["login_name"]:
            return self._status_false()

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        login_name = kwargs["login_name"]
        if User.find_by_login_name(login_name):
            return self._status_true()
        return self._status_false()

    def _status_true(self) -> str:
        return json.dumps({"status": True})

    def _status_false(self) -> str:
        return json.dumps({"status": False})
