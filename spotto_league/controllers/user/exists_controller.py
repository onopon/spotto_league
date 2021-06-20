import json
from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from spotto_league.models.user import User


class ExistsController(BaseController):
    # override
    def should_login(self) -> bool:
        return False

    # override
    def enable_for_visitor(self) -> bool:
        return True

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        if not kwargs["login_name"]:
            raise Exception()

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        login_name = kwargs["login_name"]
        if User.find_by_login_name(login_name):
            return json.dumps({"status": True})
        return json.dumps({"status": False})
