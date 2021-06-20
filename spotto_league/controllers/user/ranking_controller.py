import json
from flask import jsonify
from typing import Dict, Any
from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from spotto_league.entities.point_rank import PointRank
from datetime import datetime as dt


class RankingController(BaseController):

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        year = int(kwargs["year"])
        if dt.now().year < year:
            raise Exception("未来のランキングは見ることができません。")

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        year = int(kwargs["year"])
        point_ranks = PointRank.make_point_rank_list_in_season(year)
        return self.render_template(
            "user/ranking.html", year=year, point_ranks=point_ranks
        )

    # override
    async def get_json(self, request: BaseRequest, **kwargs) -> Dict[str, Any]:
        year = int(kwargs["year"])
        point_ranks = PointRank.make_point_rank_list_in_season(year)
        point_rank_hash = dict(
            zip([p.user.id for p in point_ranks], [p.to_hash() for p in point_ranks])
        )
        return jsonify(json.dumps({"point_rank_hash": point_rank_hash}))
