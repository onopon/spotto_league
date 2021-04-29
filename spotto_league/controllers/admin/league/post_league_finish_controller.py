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


class PostLeagueFinishController(BaseController):
    __slots__ = ['_league']
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        self._league = League.find_by_id(kwargs["league_id"])
        if not self._league:
            raise Exception("League: {} does not exist". kwargs["league_id"])
        if not self._league.is_status_ready():
            raise Exception("League status is not ready")

        if not request.form.get('league_point_group_id'):
            raise Exception("league_point_group_id does not exist")

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        session = db.session
        ranks = Rank.make_rank_list(self._league)
        group_id = request.form.get('league_point_group_id')
        league_points = LeaguePoint.find_all_by_group_id(group_id)
        bonus_points = BonusPoint.find_all_by_user_ids([r.user_id for r in ranks])
        for rank in ranks:
            league_point = next(filter(lambda l: l.rank == rank.rank, league_points), league_points[-1])
            user_point = UserPoint()
            user_point.league_id = self._league.id
            user_point.user_id = rank.user_id
            user_point.set_league_point(self._league, league_point)
            user_point.save()

            win_bonus_points = list(filter(lambda b: rank.did_win(b.user_id), bonus_points))
            for bonus_point in win_bonus_points:
                user_point = UserPoint()
                user_point.league_id = self._league.id
                user_point.user_id = rank.user_id
                user_point.set_bonus_point(bonus_point)
                user_point.save()
            self._league.league_point_group_id = group_id
            self._league.finish()
            self._league.save()
        return redirect(url_for('league_list'))
