from spotto_league.models.league import League
from spotto_league.entities.rank import Rank


class ContinuousPoint:
    # 現状2連勝 ~ 5連勝まで点数が入る。
    # 5連勝ごとにリセットするので、6連勝目は実質1勝目となりポイントは入らない。
    # プログラム的には1-5をぐるぐる回る感じにするので、その数値 * CONTINUOUS_POINT_BASE のポイントを獲得できる
    CONTINUOUS_POINT_BASE = 500
    LIMIT_COUNT_FOR_CONTINUOUS_BONUS = 4
    __slots__ = ["_user_id", "_league", "_continuous_count"]

    def __init__(self, user_id: int, league: League):
        self._user_id = user_id
        self._league = league
        self._continuous_count = self._calcurate_continuous_count()

    def _calcurate_continuous_count(self) -> int:
        count = 0
        recent_leagues = League.find_all_for_cosecutive_win_bonus_point()
        for league in recent_leagues:
            # 対象のリーグ戦より後に行われたリーグ戦は対象としない。
            if league.start_datetime >= self._league.start_datetime:
                continue
            ranks = Rank.make_rank_list(league)
            if len(ranks) > 1 and ranks[0].user_id != self._user_id:
                break
            count += 1
        return count

    @property
    def count_for_bonus(self) -> int:
        return self._continuous_count % ContinuousPoint.LIMIT_COUNT_FOR_CONTINUOUS_BONUS

    @property
    def count_for_display(self) -> int:
        return self._continuous_count + 1

    @property
    def point(self) -> int:
        return self.count_for_bonus * ContinuousPoint.CONTINUOUS_POINT_BASE
