from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask import redirect, url_for
from datetime import date


class PostModifyController(BaseController):
    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        if (self.login_user.is_admin() or self.login_user.is_member()) and not request.form.get("first-name"):
            raise Exception("管理者、チームメンバーのユーザは本名の設定は必須です。")

    async def get_layout_as_exception(
        self, request: BaseRequest, error: Exception, **kwargs
    ) -> AnyResponse:
        return self.render_template("user/modify.html", error_message=str(error))

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        self.login_user.name = request.form.get("name")
        self.login_user.first_name = request.form.get("first-name")
        self.login_user.last_name = request.form.get("last-name")
        self.login_user.gender = int(request.form["gender"])
        year = int(request.form["year"])
        month = int(request.form["month"])
        day = int(request.form["day"])
        self.login_user.birthday = date(year, month, day)
        self.login_user.save()

        return redirect(url_for("user_info", login_name=self.login_user.login_name))
