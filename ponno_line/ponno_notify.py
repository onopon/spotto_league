import requests
import settings
from typing import List, Optional
from spotto_league.models.league import League as ModelLeague
from ponno_line.templates.league_button_template import LeagueButtonTemplate
from ponno_line.messages.league_template_send_message import LeagueTemplateSendMessage

from ponno_line.templates.league_button_carousel_template import LeagueButtonCarouselTemplate


class PonnoNotify:
    NOTIFY_API = 'https://notify-api.line.me/api/notify'
    __slots__ = ['_access_token']

    def __init__(self, access_token: Optional[str] = None) -> None:
        self._access_token = access_token if access_token else settings.LINE_NOTIFY_ACCESS_TOKEN_HASH[settings.ENV]

    def notify_about_finished_league(self, league_id: int) -> None:
        league = ModelLeague.find(league_id)
        uri = "https://ponno.onopon.blog/league/{}/".format(league.id)
        texts = ["{}の結果".format(league.name)]
        texts.append(LeagueButtonTemplate().create_result_text(league))
        texts.append(uri)
        self.execute('\n'.join(texts))

    def notify_about_cancel_league(self, league_id: int) -> None:
        text = LeagueTemplateSendMessage.get_for_push_about_cacnel_league(league_id=league_id).text
        self.execute(text)

    def notify_about_join_end_at_deadline(self) -> None:
        leagues = ModelLeague.all()
        leagues.sort(key=lambda l: l.join_end_at)
        messages = []
        for l in leagues:
            if (not l.is_near_join_end_at()) or l.is_status_recruiting_near_join_end_at():
                continue
            messages.append("{}@{}".format(l.name, l.place.name))
            messages.append("日時:{}".format(l.date_for_display))
            messages.append("締切:{}".format(l.join_end_at_for_display))
            messages.append("https://ponno.onopon.blog/league/{}/".format(l.id))
            messages.append("\n")

        if not messages:
            return

        messages.pop(-1)  # 最後の \n を除く
        first_messages = ["締め切りの近い練習会があるみたいだよ！",
                          "参加表明がまだの方はお早めにね！\n"]
        self.execute('\n'.join(first_messages + messages))

    def notify_about_recruiting_league_information(self, league_ids: List[int]) -> None:
        leagues = ModelLeague.find_all_by_ids(league_ids)
        leagues.sort(key=lambda l:l.date)
        messages = []
        for l in leagues:
            messages.append("{}@{}".format(l.name, l.place.name))
            messages.append("日時:{}".format(l.date_for_display))
            messages.append("締切:{}".format(l.join_end_at_for_display))
            messages.append("https://ponno.onopon.blog/league/{}/".format(l.id))
            messages.append("\n")
        messages.pop(-1)  # 最後の \n を除く

        if not messages:
            return
        first_messages = ["募集中の練習会が追加されたみたいだよ！",
                          "ご都合の合う方はどしどし参加表明ボタンを押してね！\n"]
        self.execute('\n'.join(first_messages + messages))

    def execute(self, text: str):
        if not self._access_token:
            return
        message = '\n' + text
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + self._access_token}
        requests.post(PonnoNotify.NOTIFY_API, data=payload, headers=headers)
