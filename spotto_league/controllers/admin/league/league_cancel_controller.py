import asyncio
import json
from typing import Dict, Any, List
from collections import defaultdict
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template, redirect, url_for
from flask_login import current_user
from spotto_league.entities.rank import Rank
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_point import LeaguePoint
from spotto_league.models.bonus_point import BonusPoint
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail
from spotto_league.models.user_point import UserPoint
from spotto_league.database import db
from ponno_linebot.ponno_bot import PonnoBot

INVALID_MATCH_GROUP_ID = 0


class LeagueCancelController(BaseController):
    __slots__ = ['_league']
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        self._league = League.find_by_id(kwargs["league_id"])
        if not self._league:
            raise Exception("League: {} does not exist". kwargs["league_id"])
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
        return redirect(url_for('league_list'))