from typing import Optional
from flask import url_for
from linebot.models.template import Template, CarouselTemplate

from ponno_linebot.templates.base import Base
from ponno_linebot.carousel_columns.league_button_carousel_column import LeagueButtonCarouselColumn
from spotto_league.models.league import League as ModelLeague
from spotto_league.entities.rank import Rank

COLUMN_MAX_COUNT = 10


class LeagueButtonCarouselTemplate(Base):
    # override
    def create(self, **kwargs) -> Optional[Template]:
        leagues = ModelLeague.all()
        columns = []
        for l in leagues:
            if not l.is_near_join_end_at():
                continue
            _kwargs = kwargs
            _kwargs["league"] = l
            column = LeagueButtonCarouselColumn().create(**_kwargs)
            columns.append(column)
            if len(columns) > COLUMN_MAX_COUNT:
                break
        if not columns:
            return None
        return CarouselTemplate(columns = columns)
