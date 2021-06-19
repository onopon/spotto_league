from spotto_league.controllers.base_controller import BaseController, AnyResponse
from werkzeug.wrappers import BaseRequest
from ponno_line.ponno_bot import PonnoBot


class PostNotifyRecruitingController(BaseController):
    # override
    async def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    # override
    async def get_layout(self, request: BaseRequest, **kwargs) -> AnyResponse:
        league_ids = [int(l_id) for l_id in request.form.getlist("league_ids[]")]
        PonnoBot.push_about_recruiting_league_information(league_ids)
        return "success"
