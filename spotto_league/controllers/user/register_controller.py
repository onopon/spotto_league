from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from spotto_league.models.user import User


class RegisterController(BaseController):
    # override
    def should_login(self) -> bool:
        return False

    # override
    def enable_for_visitor(self) -> bool:
        return True

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        return self.render_template("user/register.html", login_user=User())
