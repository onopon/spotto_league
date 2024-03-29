from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask_login import current_user
from spotto_league.models.user import User
from spotto_league.models.place import Place


class RegisterController(BaseController):
    __slots__ = ["_user"]

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        self._user = User.find_by_login_name(current_user.login_name)
        if not self._user:
            raise Exception("User: {} does not exist.".format(current_user.login_name))
        if not self._user.is_admin():
            raise Exception("User: {} is not admin.".format(current_user.login_name))

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        places = Place.all()
        return self.render_template("admin/league/register.html", places=places)
