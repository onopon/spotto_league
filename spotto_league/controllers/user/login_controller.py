from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask import redirect, url_for
from flask_login import current_user


class LoginController(BaseController):
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
        if current_user.is_authenticated:
            return redirect(url_for("league_list"))
        return self.render_template("user/login.html")
