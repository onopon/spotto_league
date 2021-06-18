import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import redirect, url_for
from spotto_league.models.league import League
from ponno_line.ponno_bot import PonnoBot


class LeagueCancelController(BaseController):
    __slots__ = ["_league"]

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        self._league = League.find_by_id(kwargs["league_id"])
        if not self._league:
            raise Exception("League: {} does not exist".kwargs["league_id"])
        if self._league.is_in_session():
            raise Exception("League status is in session. So it can not cancel.")
        if self._league.is_status_finished():
            raise Exception("League status is still finished.")

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        self._league.cancel()
        self._league.save()
        PonnoBot.push_about_cancel_league(self._league.id)
        return redirect(url_for("league_list"))
