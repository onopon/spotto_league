from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask import redirect, url_for
from spotto_league.models.user import User
from spotto_league.modules.password_util import PasswordUtil
import flask_login


class PostLoginController(BaseController):
    __slots__ = ["_user"]

    # override
    def should_login(self) -> bool:
        return False

    # override
    def enable_for_visitor(self) -> bool:
        return True

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        login_name = request.form.get("login_name", "")
        password = request.form.get("password", "")
        common_password = request.form.get("common_password", "")

        # Visitor用validate
        if PasswordUtil.is_correct_common_visitor_password(common_password):
            user = User.find_by_login_name(login_name)
            if not user:
                raise Exception("ログイン失敗")
            if not PasswordUtil.is_same(password, user.password):
                raise Exception("ログイン失敗")
            if not user.is_visitor():
                raise Exception("ログイン失敗")
            if user.is_withdrawaler():
                raise Exception("ログイン失敗")
        # それ以外の人用validate
        elif PasswordUtil.is_correct_common_password(common_password):
            user = User.find_by_login_name(login_name)
            if not user:
                raise Exception("ログイン失敗")
            if not PasswordUtil.is_same(password, user.password):
                raise Exception("ログイン失敗")
            if user.is_visitor() or user.is_withdrawaler():
                raise Exception("ログイン失敗")
        else:
            raise Exception("ログイン失敗")
        self._user = user

    async def get_layout_as_exception(
        self, request: BaseRequest, error: Exception, **kwargs
    ) -> AnyResponse:
        return self.render_template("user/login.html", is_miss_login=True)

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        user = User()
        user.id = self._user.login_name
        user.login_name = self._user.login_name
        remember = True if not self._user.is_visitor() else False
        flask_login.login_user(user, remember=remember)
        return redirect(url_for("league_list"))
