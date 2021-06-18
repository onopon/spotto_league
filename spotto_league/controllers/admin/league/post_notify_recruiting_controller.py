import asyncio
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from ponno_line.ponno_bot import PonnoBot


class PostNotifyRecruitingController(BaseController):
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        pass

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        league_ids = [int(l_id) for l_id in request.form.getlist("league_ids[]")]
        PonnoBot.push_about_recruiting_league_information(league_ids)
        return "success"
