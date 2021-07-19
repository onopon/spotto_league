from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask_login import current_user
from spotto_league.models.user import User
from spotto_league.models.role import RoleType
from spotto_league.exceptions import NotAdminException


class ListController(BaseController):
    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        if not self.login_user.is_admin():
            raise NotAdminException("User: {} is not admin.".format(current_user.login_name))

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        users = User.all_without_visitor()
        role_type_hash_list = RoleType.all()
        return self.render_template(
            "admin/user/list.html", users=users, role_type_hash_list=role_type_hash_list
        )
