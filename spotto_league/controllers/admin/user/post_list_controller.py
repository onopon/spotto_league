from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask_login import current_user
from spotto_league.models.user import User
from spotto_league.models.role import Role, RoleType
from spotto_league.models.unpaid import Unpaid
from spotto_league.database import db

ROLE_TYPE_GUEST = -1


class PostListController(BaseController):
    __slots__ = ["_users"]

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        if not self.login_user.is_admin():
            raise Exception("User: {} is not admin.".format(current_user.login_name))

        self._users = User.all_without_visitor()
        for user in self._users:
            role_type_key = "radio_{}".format(user.login_name)
            role_type_value = int(request.form.get(role_type_key, -1))
            if (
                self.login_user.id == user.id
                and role_type_value != RoleType.ADMIN.value
            ):
                raise Exception("自分自身を管理者以外に設定することはできません。")
            if (not user.first_name or not user.last_name) and role_type_value in [RoleType.ADMIN.value, RoleType.MEMBER.value]:
                raise Exception("名前の設定がないユーザに役柄を設定することはできません。")

    async def get_layout_as_exception(
        self, request: BaseRequest, error: Exception, **kwargs
    ) -> AnyResponse:
        role_type_hash_list = RoleType.all()
        return self.render_template(
            "admin/user/list.html",
            users=self._users,
            role_type_hash_list=role_type_hash_list,
            error_message=str(error),
        )

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        role_type_hash_list = RoleType.all()
        session = db.session
        for user in self._users:
            role_type_key = "radio_{}".format(user.login_name)
            role_type_value = int(request.form[role_type_key])
            if role_type_value == ROLE_TYPE_GUEST:
                if user.role.id:
                    session.delete(user.role)
                continue
            role = user.role or Role()
            role.user_id = user.id
            role.role_type = role_type_value
            session.add(role)

            unpaid_key = "unpaid_{}".format(user.login_name)
            unpaid_value = int(request.form[unpaid_key] or 0)
            unpaid = Unpaid.find_or_initialize_by_user_id(user.id)
            if unpaid_value > 0:
                memo_key = "unpaid_memo_{}".format(user.login_name)
                memo_value = request.form[memo_key]
                unpaid.amount = unpaid_value
                unpaid.memo = memo_value
                session.add(unpaid)
            else:
                if unpaid.id:
                    session.delete(unpaid)
        session.commit()
        return self.render_template(
            "admin/user/list.html",
            users=self._users,
            role_type_hash_list=role_type_hash_list,
            is_success=True,
        )
