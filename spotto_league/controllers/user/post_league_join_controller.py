import json
from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask import jsonify
from spotto_league.models.league import League
from spotto_league.models.user import User
from spotto_league.models.league_member import LeagueMember


class PostLeagueJoinController(BaseController):
    # override
    def enable_for_visitor(self) -> bool:
        return True

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        league_id = int(request.form.get("league_id", 0))
        try:
            League.find(league_id)
        except Exception:
            raise Exception("League: {} does not exist.".format(league_id))

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        league_id = int(request.form["league_id"])
        user_id = self.login_user.id
        login_name = request.form.get("login_name", None)
        if login_name:
            user = User.find_by_login_name(login_name)
            if not user:
                return jsonify(json.dumps({"result": "failure", "cause": "{} does not found.".format(login_name)}))
            user_id = user.id
        league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(
            league_id, user_id
        )
        if request.form.get("force_join"):
            league_member.enabled = True
        league_member.save()
        return jsonify(json.dumps({"result": "success"}))
