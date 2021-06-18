import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask_login import current_user
from spotto_league.models.league import League
from spotto_league.models.place import Place


class ModifyController(BaseController):
    __slots__ = ["_league"]

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        if not self.login_user.is_admin():
            raise Exception("User: {} is not admin.".format(current_user.login_name))
        league_id = request.args.get("id", 0)
        self._league = League.find_by_id(league_id)
        if self._league is None:
            raise Exception("League: {} is not found.".format(league_id))

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        places = Place.all()
        return self.render_template(
            "admin/league/register.html", places=places, league=self._league
        )
