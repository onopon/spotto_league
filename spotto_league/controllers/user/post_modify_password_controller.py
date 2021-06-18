import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import redirect, url_for


class PostModifyPasswordController(BaseController):
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            raise Exception("パスワードが一致しません。")

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        self.login_user.set_password(request.form.get("password"))
        self.login_user.save()

        return redirect(url_for("user_info", login_name=self.login_user.login_name))
