from typing import Optional
from ponno_line.messages.base import Base
from linebot.models import Message, TextSendMessage, TemplateSendMessage
from ponno_line.templates.league_button_template import LeagueButtonTemplate
from ponno_line.templates.league_button_carousel_template import (
    LeagueButtonCarouselTemplate,
)
from spotto_league.models.league import League as ModelLeague
from datetime import date, timedelta


class LeagueTemplateSendMessage(Base):
    # override
    def satisfy_react_condition(self, **kwargs) -> bool:
        return False

    # override
    def create(self, **kwargs) -> Optional[Message]:
        return None

    @classmethod
    def get_for_push_about_finished_league(cls, **kwargs) -> Optional[Message]:
        league_id = kwargs["league_id"]
        league = ModelLeague.find(league_id)
        kwargs["league"] = league
        return TemplateSendMessage(
            alt_text="{}の結果をお送りします。".format(league.name),
            template=LeagueButtonTemplate().create(**kwargs),
        )

    @classmethod
    def get_for_push_about_cacnel_league(cls, **kwargs) -> Optional[Message]:
        league_id = kwargs["league_id"]
        league = ModelLeague.find(league_id)
        kwargs["league"] = league
        texts = ["{}開催予定の「{}」は中止となりました。\n".format(league.date_for_display, league.name)]
        user_names = ["{}さん".format(m.user.name) for m in league.members]
        if user_names:
            texts.append("参加表明を出していた")
            texts.extend(user_names)
        texts.append("申し訳ございません。")
        return TextSendMessage(text="\n".join(texts))

    @classmethod
    def get_for_push_about_join_end_at_deadline(cls, **kwargs) -> Optional[Message]:
        template = LeagueButtonCarouselTemplate().create(**kwargs)
        if not template:
            return None
        return TemplateSendMessage(alt_text="参加締め切りの近い練習会をお知らせします。", template=template)

    @classmethod
    def get_for_push_about_recruiting_leagues(cls, **kwargs) -> Optional[Message]:
        _ = kwargs["league_ids"]
        kwargs["is_recruiting"] = True
        template = LeagueButtonCarouselTemplate().create(**kwargs)
        if not template:
            return None
        return TemplateSendMessage(alt_text="募集中の練習会をお知らせします。", template=template)

    @classmethod
    def get_for_push_about_league_day_before(cls, **kwargs) -> Optional[Message]:
        text = cls.get_for_push_about_league_day_before_text()
        if not text:
            return None
        return TextSendMessage(text=text)

    @classmethod
    def get_for_push_about_league_day_before_text(cls, **kwargs) -> Optional[str]:
        leagues = ModelLeague.all()
        leagues.sort(key=lambda l: l.start_at)
        columns = []
        tomorrow = date.today() + timedelta(days=1)
        leagues = [l for l in leagues if l.is_status_ready() and l.date == tomorrow]
        if not leagues:
            return None

        texts = ["明日は練習会です！みんな頑張ってねっ！"]
        for league in leagues:
            texts.append("\n○{}".format(league.name))
            texts.append("日時:{}".format(league.date_for_display))
            texts.append("場所:{}".format(league.place.name))
            texts.append("詳細: https://ponno.onopon.blog/league/{}/".format(league.id))
            texts.append("参加者:")
            user_names = ["{}さん".format(m.user.name) for m in league.members if m.enabled]
            texts.extend(user_names)
        return "\n".join(texts)
