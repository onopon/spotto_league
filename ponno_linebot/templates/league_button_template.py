from flask import url_for
from linebot.models.template import Template, ButtonsTemplate

from ponno_linebot.templates.base import Base
from ponno_linebot.actions.detail_uri_action import DetailURIAction
from spotto_league.models.league import League as ModelLeague
from spotto_league.entities.rank import Rank

class LeagueButtonTemplate(Base):
    # override
    def create(self, **kwargs) -> Template:
        league = kwargs["league"]
        uri = "https://ponno.onopon.blog/{}".format(url_for('league', league_id = league.id))
        return ButtonsTemplate(
                text = self._create_text(league),
                title = "{} の結果".format(league.name),
                actions = [DetailURIAction().create(uri = uri)]
                )

    # 3行までしか表示できない
    def _create_text(self, league: ModelLeague) -> str:
        ranks = Rank.make_rank_list(league)  # ranksが空にならないことを信用する
        texts = []
        texts.append("今回の優勝は")
        r = ranks[0]
        texts.append("{}勝{}敗 {}さん".format(r.win, r.lose, r.user.name))
        texts.append("でした。おめでとうございます！")
        return '\n'.join(texts)
