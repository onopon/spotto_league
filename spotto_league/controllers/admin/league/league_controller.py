import asyncio
import json
from typing import Dict, Any, List
from collections import defaultdict
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template
from flask_login import current_user
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail


class LeagueController(BaseController):
    __slots__ = ['_league']
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        self._league = League.find_by_id(kwargs["league_id"])
        if not self._league:
            raise Exception

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        return self.render_template("admin/league/league.html", league=self._league)
