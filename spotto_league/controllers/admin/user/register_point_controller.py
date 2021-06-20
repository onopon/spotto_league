from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask_login import current_user
from spotto_league.models.user import User
from spotto_league.models.bonus_point import BonusPoint


class RegisterPointController(BaseController):
    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        if not self.login_user.is_admin():
            raise Exception("User: {} is not admin.".format(current_user.login_name))

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        users = User.all()
        bonus_points = BonusPoint.all()
        return self.render_template(
            "admin/user/register_point.html", users=users, bonus_points=bonus_points
        )
