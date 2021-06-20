from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask import redirect, url_for
from spotto_league.models.league import League
from ponno_line.ponno_bot import PonnoBot


class LeagueCancelController(BaseController):
    __slots__ = ["_league"]

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        try:
            self._league = League.find(kwargs["league_id"])
            if self._league.is_in_session():
                raise Exception("League status is in session. So it can not cancel.")
            if self._league.is_status_finished():
                raise Exception("League status is still finished.")
        except Exception as e:
            raise e

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        self._league.cancel()
        self._league.save()
        PonnoBot.push_about_cancel_league(self._league.id)
        return redirect(url_for("league_list"))
