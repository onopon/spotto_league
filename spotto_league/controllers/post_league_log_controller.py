import json
from typing import Optional
from flask import jsonify
from .base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail


class PostLeagueLogController(BaseController):
    __slots__ = ["_league_log"]

    def __init__(self) -> None:
        super().__init__()
        self._league_log: Optional[LeagueLog] = None

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        league_id = int(request.form["league_id"])
        user_id_1 = int(request.form["user_id_1"])
        user_id_2 = int(request.form["user_id_2"])
        score_1_list = [int(s or 0) for s in request.form.getlist("score_1_list[]")]
        score_2_list = [int(s or 0) for s in request.form.getlist("score_2_list[]")]
        if not all([league_id, user_id_1, user_id_2]):
            raise Exception("All data does not exist.")

        if (
            not score_1_list
            or not score_2_list
            or len(score_1_list) != len(score_2_list)
        ):
            raise Exception("Score List is invalid.")

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        league_id = int(request.form["league_id"])
        user_id_1 = int(request.form["user_id_1"])
        user_id_2 = int(request.form["user_id_2"])
        self._league_log = LeagueLog.find_or_initialize(league_id, user_id_1, user_id_2)
        if not self._league_log.id:
            self._league_log.save()
        is_reverse = user_id_1 != self._league_log.user_id_1

        score_1_list = [int(s or 0) for s in request.form.getlist("score_1_list[]")]
        score_2_list = [int(s or 0) for s in request.form.getlist("score_2_list[]")]
        league_log_details = self._league_log.details
        for i, (score_1, score_2) in enumerate(zip(score_1_list, score_2_list)):
            try:
                detail = league_log_details[i]
            except Exception:
                detail = LeagueLogDetail()
            finally:
                detail.league_log_id = self._league_log.id
                if not is_reverse:
                    detail.score_1 = score_1
                    detail.score_2 = score_2
                else:
                    detail.score_1 = score_2
                    detail.score_2 = score_1
            if detail.is_zero_all():
                detail.delete()
                continue
            detail.save()
        return jsonify(json.dumps(self._get_league_log_hash()))

    def _get_league_log_hash(self):
        details = self._league_log.details
        count_1 = [d.score_1 > d.score_2 for d in details].count(True)
        count_2 = [d.score_1 < d.score_2 for d in details].count(True)
        details_hash_list = [
            {"score_1": d.score_1, "score_2": d.score_2} for d in details
        ]
        reverse_details_hash_list = [
            {"score_1": d.score_2, "score_2": d.score_1} for d in details
        ]

        league_log_hash = {}
        league_log_hash[
            "{}-{}".format(self._league_log.user_id_1, self._league_log.user_id_2)
        ] = {
            "user_id_1": self._league_log.user_id_1,
            "user_id_2": self._league_log.user_id_2,
            "count_1": count_1,
            "count_2": count_2,
            "details_hash_list": details_hash_list,
        }
        league_log_hash[
            "{}-{}".format(self._league_log.user_id_2, self._league_log.user_id_1)
        ] = {
            "user_id_1": self._league_log.user_id_2,
            "user_id_2": self._league_log.user_id_1,
            "count_1": count_2,
            "count_2": count_1,
            "details_hash_list": reverse_details_hash_list,
        }
        return league_log_hash
