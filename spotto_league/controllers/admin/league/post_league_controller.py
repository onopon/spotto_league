from spotto_league.controllers.base_controller import BaseController, AnyResponse
from spotto_league.exceptions import (
    UnexpectedLeagueStatusException,
    UnexpectedArgsException,
    UnexpectedValueException
)
from werkzeug.wrappers import BaseRequest
from flask import redirect, url_for
from flask_login import current_user
from spotto_league.models.league import League
from spotto_league.database import db

# TODO: リーグ戦最低人数を決める
MIN_MEMBER_LIMIT = 2


class PostLeagueController(BaseController):
    __slots__ = ["_league"]

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        league = League.find_by_id(kwargs["league_id"])
        if not league:
            raise UnexpectedArgsException("league_id :{} does not exist".format(kwargs["league_id"]))

        if league.is_status_finished():
            raise UnexpectedLeagueStatusException("League status is finished")

        league_member_ids = request.form.getlist("enabled_league_member_ids")
        if len(league_member_ids) < MIN_MEMBER_LIMIT:
            raise UnexpectedValueException("League member less than {}".format(MIN_MEMBER_LIMIT))
        self._league = league

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        session = db.session
        league_member_ids = [
            int(m_id) for m_id in request.form.getlist("enabled_league_member_ids")
        ]
        for member in self._league.members:
            if member.id in league_member_ids:
                member.enabled = True
            else:
                member.enabled = False
            session.add(member)
        self._league.ready()
        session.add(self._league)
        session.commit()
        return redirect(url_for("league_list", login_name=current_user.login_name))
