import asyncio
import json
from typing import Dict, Any
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, redirect, url_for
from flask_login import current_user
from spotto_league.models.user import User
from spotto_league.models.league import League, LeagueStatus
from spotto_league.entities.point_rank import PointRank
from datetime import datetime as dt


class RankingController(BaseController):

    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        year = int(kwargs["year"])
        if dt.now().year < year:
            raise Exception('未来のランキングは見ることができません。')

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        year = int(kwargs["year"])
        users = User.all()
        point_ranks = PointRank.make_point_rank_list_in_season(year)
        return self.render_template("user/ranking.html", year=year, point_ranks=point_ranks)

    # override
    @asyncio.coroutine
    def get_json(self, request: BaseRequest, **kwargs) -> Dict[str, Any]:
        year = int(kwargs["year"])
        point_ranks = PointRank.make_point_rank_list_in_season(year)
        point_rank_hash = dict(zip([p.user.id for p in point_ranks], [p.to_hash() for p in point_ranks]))
        return json.dumps({'point_rank_hash': point_rank_hash})
