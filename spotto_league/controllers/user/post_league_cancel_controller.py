from flask import jsonify
from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember


class PostLeagueCancelController(BaseController):
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
        league_id = request.form["league_id"]
        league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(
            league_id, self.login_user.id
        )
        league_member.delete()
        return jsonify({"result": "success"})
