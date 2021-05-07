from typing import Optional
from ponno_linebot.messages.base import Base
from linebot.models import (
    Message,
    TemplateSendMessage
)
from ponno_linebot.templates.league_button_template import LeagueButtonTemplate
from ponno_linebot.templates.league_button_carousel_template import LeagueButtonCarouselTemplate
from spotto_league.models.league import League as ModelLeague


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
        return TemplateSendMessage(alt_text="{}の結果をお送りします。".format(league.name),
                                   template=LeagueButtonTemplate().create(**kwargs))

    @classmethod
    def get_for_push_about_join_end_at_deadline(cls, **kwargs) -> Optional[Message]:
        template = LeagueButtonCarouselTemplate().create(**kwargs)
        if not template:
            return None
        return TemplateSendMessage(alt_text="参加締め切りの近いリーグ戦をお知らせします。",
                                   template=template)
