from typing import Any, Dict
from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from spotto_league.models.user import User
from spotto_league.models.league import League
from spotto_league.entities.point_rank import PointRank
from datetime import datetime as dt


class InfoController(BaseController):
    __slots__ = ["_user"]

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        user = User.find_by_login_name(kwargs["login_name"])
        if not user:
            raise Exception("{}というユーザは存在しません。".format(kwargs["login_name"]))

        if user.is_visitor():
            raise Exception(
                "ビジターアカウントはの情報は見ることができません。{}の誕生日は{}だよ。".format(
                    user.name, user.birthday_for_display
                )
            )
        self._user = user

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        date = dt.now().date()
        render_hash: Dict[str, Any] = {}
        render_hash["is_update_for_admin"] = int(
            request.form.get("is_update_for_admin", 0)
        )
        render_hash["year"] = date.year
        render_hash["user"] = self._user
        point_rank_list = PointRank.make_point_rank_list_in_season(date.year)
        render_hash["point_rank"] = next(
            (pr for pr in point_rank_list if pr.user.id == self._user.id), None
        )
        if self._user.id == self.login_user.id:
            if self.login_user.is_admin():
                leagues = League.all()
                leagues.sort(key=lambda r: r.date, reverse=False)
                render_hash["yet_recruiting_league_list"] = []
                render_hash["ready_league_list"] = []
                render_hash["yet_finished_league_list"] = []
                for league in leagues:
                    if league.is_status_recruiting():
                        render_hash["yet_recruiting_league_list"].append(league)
                    elif league.is_status_ready():
                        if league.date <= date:
                            render_hash["yet_finished_league_list"].append(league)
                        else:
                            render_hash["ready_league_list"].append(league)
        return self.render_template("user/info.html", **render_hash)
