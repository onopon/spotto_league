from .base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember
from collections import defaultdict


class LeagueListController(BaseController):
    # override
    def enable_for_visitor(self) -> bool:
        return True

    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        is_from_register = bool(request.form.get("is_from_register", 0))
        league_list = League.all()
        league_list.sort(key=lambda r: r.date, reverse=False)

        league_list_hash = defaultdict(list)
        league_members = LeagueMember.find_all_by_user_id(self.login_user.id)
        user_join_league_ids = []
        user_join_enable_league_ids = []
        user_join_disable_league_ids = []
        for lm in league_members:
            user_join_league_ids.append(lm.league_id)
            if lm.enabled:
                user_join_enable_league_ids.append(lm.league_id)
            else:
                user_join_disable_league_ids.append(lm.league_id)
        for league in league_list:
            if league.is_on_today():
                league_list_hash["today"].append(league)
            elif league.is_status_recruiting():
                league_list_hash["status_recruiting"].append(league)
            elif league.is_status_ready():
                if league.is_after_session():
                    league_list_hash["status_finished"].append(league)
                else:
                    league_list_hash["status_ready"].append(league)
            elif league.is_status_finished():
                league_list_hash["status_finished"].append(league)
        league_list_hash["status_finished"].sort(key=lambda r: r.date, reverse=True)
        return self.render_template(
            "league_list.html",
            is_from_register=is_from_register,
            user_join_league_ids=user_join_league_ids,
            user_join_enable_league_ids=user_join_enable_league_ids,
            user_join_disable_league_ids=user_join_disable_league_ids,
            league_list_hash=league_list_hash,
        )
