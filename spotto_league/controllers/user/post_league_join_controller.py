import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import jsonify
from spotto_league.models.league import League
from spotto_league.models.user import User
from spotto_league.models.league_member import LeagueMember


class PostLeagueJoinController(BaseController):
    # override
    def enable_for_visitor(self) -> bool:
        return True

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        league_id = int(request.form.get("league_id", 0))
        try:
            League.find(league_id)
        except Exception:
            raise Exception("League: {} does not exist.".format(league_id))

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        league_id = int(request.form["league_id"])
        user_id = self.login_user.id
        login_name = request.form.get("login_name", None)
        if login_name:
            try:
                user_id = User.find(login_name).id
            except Exception:
                return jsonify({"result": "failure", "cause": "{} does not found.".format(login_name)})
        league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(
            league_id, user_id
        )
        if request.form.get("force_join"):
            league_member.enabled = True
        league_member.save()
        return jsonify({"result": "success"})
