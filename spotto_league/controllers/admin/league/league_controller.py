from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask_login import current_user
from spotto_league.models.league import League
from spotto_league.entities.rank import Rank
from spotto_league.models.user import User


class LeagueController(BaseController):
    __slots__ = ["_league"]

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        if not self.login_user.is_admin():
            raise Exception("User: {} is not admin.".format(current_user.login_name))
        try:
            self._league = League.find(kwargs["league_id"])
        except Exception as e:
            raise e

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        rank_list = Rank.make_rank_list(self._league)
        league_member_user_ids = [m.user_id for m in self._league.members]
        users = [u for u in User.all() if u.id not in league_member_user_ids]
        return self.render_template(
            "admin/league/league.html",
            league=self._league,
            rank_list=rank_list,
            users=users,
        )
