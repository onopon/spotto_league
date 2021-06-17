from typing import Optional
from linebot.models import CarouselColumn
from ponno_line.carousel_columns.base import Base
from ponno_line.actions.detail_uri_action import DetailURIAction
from spotto_league.models.league import League as ModelLeague


class LeagueButtonCarouselColumn(Base):
    # override
    def create(self, **kwargs) -> Optional[CarouselColumn]:
        league = kwargs["league"]
        uri = "https://ponno.onopon.blog/league/{}/".format(league.id)
        title = "{}@{}".format(league.name, league.place.name)
        text = self._create_near_join_end_at_text(league)

        return CarouselColumn(
            text=text,
            title=title,
            actions=[DetailURIAction().create(uri=uri)]
        )

    # 3行までしか表示できない
    # 60文字までしか表示できない
    def _create_near_join_end_at_text(self, league: ModelLeague) -> str:
        texts = []
        texts.append("日時:{}".format(league.date_for_display))
        texts.append("締切:{}".format(league.join_end_at_for_display))
        return '\n'.join(texts)
