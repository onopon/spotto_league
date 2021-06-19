from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask import redirect, url_for


class PostModifyPasswordController(BaseController):
    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            raise Exception("パスワードが一致しません。")

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        self.login_user.set_password(request.form.get("password"))
        self.login_user.save()

        return redirect(url_for("user_info", login_name=self.login_user.login_name))
