import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask_login import current_user
from spotto_league.models.league import League
from spotto_league.entities.rank import Rank
from spotto_league.models.user import User


class LeagueController(BaseController):
    __slots__ = ["_league"]

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        if not self.login_user.is_admin():
            raise Exception("User: {} is not admin.".format(current_user.login_name))
        self._league = League.find_by_id(kwargs["league_id"])
        if not self._league:
            raise Exception("League: {} does not exist.".format(kwargs["league_id"]))

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        rank_list = Rank.make_rank_list(self._league)
        league_member_user_ids = [m.user_id for m in self._league.members]
        users = [u for u in User.all() if u.id not in league_member_user_ids]
        return self.render_template(
            "admin/league/league.html",
            league=self._league,
            rank_list=rank_list,
            users=users,
        )
