from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from flask import redirect, url_for
from spotto_league.entities.rank import Rank
from spotto_league.models.league import League
from spotto_league.models.league_point import LeaguePoint
from spotto_league.models.bonus_point import BonusPoint
from spotto_league.models.user_point import UserPoint
from ponno_line.ponno_bot import PonnoBot

INVALID_MATCH_GROUP_ID = 0


class PostLeagueFinishController(BaseController):
    __slots__ = ["_league"]

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        try:
            self._league = League.find(kwargs["league_id"])
            if not self._league.is_status_ready():
                raise Exception("League status is not ready")
            if request.form.get("league_point_group_id") is None:
                raise Exception("league_point_group_id does not exist")
        except Exception as e:
            raise e

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        # session = db.session
        ranks = Rank.make_rank_list(self._league)
        group_id = int(request.form.get("league_point_group_id", 0))

        league_points = LeaguePoint.find_all_by_group_id(group_id)
        bonus_points = BonusPoint.find_all_by_user_ids([r.user_id for r in ranks])
        for rank in ranks:
            if rank.user.is_guest() or rank.user.is_visitor():
                continue
            league_point = next(
                filter(lambda l: l.rank == rank.rank, league_points), league_points[-1]
            )
            user_point = UserPoint()
            user_point.league_id = self._league.id
            user_point.user_id = rank.user_id
            user_point.set_league_point(self._league, league_point)
            user_point.save()

            # group_id が 0（無効試合）だった場合、bonus_pointの付与も行わない
            if group_id == INVALID_MATCH_GROUP_ID:
                continue

            win_bonus_points = list(
                filter(lambda b: rank.won(b.user_id), bonus_points)
            )
            for bonus_point in win_bonus_points:
                user_point = UserPoint()
                user_point.league_id = self._league.id
                user_point.user_id = rank.user_id
                user_point.set_bonus_point(bonus_point)
                user_point.save()
            self._league.league_point_group_id = group_id
            self._league.finish()
            self._league.save()
        PonnoBot.push_about_finished_league(self._league.id)
        return redirect(url_for("league_list"))
