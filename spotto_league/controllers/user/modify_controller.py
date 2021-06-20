from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest


class ModifyController(BaseController):
    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        return self.render_template("user/modify.html")
