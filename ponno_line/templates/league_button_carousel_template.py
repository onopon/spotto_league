from typing import Optional, List
from linebot.models.template import Template, CarouselTemplate, CarouselColumn

from ponno_line.templates.base import Base
from ponno_line.carousel_columns.league_button_carousel_column import (
    LeagueButtonCarouselColumn,
)
from spotto_league.models.league import League as ModelLeague

COLUMN_MAX_COUNT = 10


class LeagueButtonCarouselTemplate(Base):
    # override
    def create(self, **kwargs) -> Optional[Template]:
        columns = []
        if kwargs.get("is_recruiting", False):
            columns = self._make_recruiting_league_columns(**kwargs)
        else:
            columns = self._make_near_join_end_at_league_columns(**kwargs)
        if not columns:
            return None
        return CarouselTemplate(columns=columns)

    def _make_near_join_end_at_league_columns(self, **kwargs) -> List[CarouselColumn]:
        leagues = ModelLeague.all()
        leagues.sort(key=lambda l: l.join_end_at)
        columns = []
        for l in leagues:
            if (
                not l.is_near_join_end_at()
            ) or l.is_status_recruiting_near_join_end_at():
                continue
            _kwargs = kwargs
            _kwargs["league"] = l
            column = LeagueButtonCarouselColumn().create(**_kwargs)
            columns.append(column)
            if len(columns) > COLUMN_MAX_COUNT:
                break
        return columns

    def _make_recruiting_league_columns(self, **kwargs) -> List[CarouselColumn]:
        leagues = ModelLeague.find_all_by_ids(kwargs.get("league_ids", []))
        leagues.sort(key=lambda l: l.date)
        columns = []
        for l in leagues:
            if not (l.is_status_recruiting() and l.is_in_join_session()):
                continue
            _kwargs = kwargs
            _kwargs["league"] = l
            column = LeagueButtonCarouselColumn().create(**_kwargs)
            columns.append(column)
            if len(columns) > COLUMN_MAX_COUNT:
                break
        return columns
