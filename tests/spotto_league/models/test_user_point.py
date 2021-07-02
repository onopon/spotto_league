from spotto_league.models.user_point import (
    UserPoint,
    REASON_CLASS_BASE,
    REASON_CLASS_LEAGUE,
    REASON_CLASS_BONUS
)
from spotto_league.models.bonus_point import BonusPoint
from spotto_league.models.league_point import LeaguePoint
from tests.base import Base
from tests.modules.data_creator import DataCreator
import freezegun


class TestUserPoint(Base):
    def test_set_base_point(self):
        user_point = UserPoint()
        point = 100
        memo = 'memo'
        user_point.set_base_point(point, memo)
        assert user_point.point == point
        assert user_point.reason_class == REASON_CLASS_BASE
        assert user_point.memo == memo

    def test_set_league_point(self):
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id})
        league_point = LeaguePoint()
        league_point.point = 100
        user_point = UserPoint()
        user_point.set_league_point(league, league_point)
        assert user_point.point == league_point.point
        assert user_point.reason_class == REASON_CLASS_LEAGUE
        assert user_point.reason_id == league.id

    def test_set_bonus_point(self):
        user_id = 1
        bonus_point = BonusPoint()
        bonus_point.user_id = user_id
        bonus_point.point = 1500
        bonus_point.available_count = 10
        bonus_point.save()

        user_point = UserPoint()
        user_point.set_bonus_point(bonus_point)
        assert user_point.point == bonus_point.point
        assert user_point.reason_class == REASON_CLASS_BONUS
        assert user_point.reason_id == bonus_point.id

    def test_set_point(self):
        user_point = UserPoint()
        point = 100
        reason_class = 'Reason'
        memo = 'memo'

        user_point = UserPoint()
        user_point.set_point(point, reason_class, memo)
        assert user_point.point == point
        assert user_point.reason_class == reason_class
        assert user_point.memo == memo

    def test_find_all_in_season(self):
        place = DataCreator().create('place')
        users = DataCreator().create('two_member_users')
        with freezegun.freeze_time('2020-12-31 23:59:59'):
            user = users[0]
            league = DataCreator().create('default_league', overrided_dict={'place_id': place.id})
            user_point_2020 = UserPoint()
            user_point_2020.user_id = user.id
            user_point_2020.league_id = league.id
            user_point_2020.set_point(100, 'Hoge', '2020-12-31 23:59:59')
            user_point_2020.created_at = '2020-12-31 23:59:59'
            user_point_2020.save()

        with freezegun.freeze_time('2021-01-01 00:00:00'):
            user = users[1]
            league = DataCreator().create('default_league', overrided_dict={'place_id': place.id})
            user_point_2021 = UserPoint()
            user_point_2021.user_id = user.id
            user_point_2021.league_id = league.id
            user_point_2021.set_point(100, 'Hoge', '2021-01-01 00:00:00')
            user_point_2021.created_at = '2021-01-01 00:00:00'
            user_point_2021.save()

        with freezegun.freeze_time('2021-07-02 00:00:00'):
            assert UserPoint.find_all_in_season(2019) == []
            assert UserPoint.find_all_in_season(2020) == [user_point_2020]
            assert UserPoint.find_all_in_season(2021) == [user_point_2021]
            assert UserPoint.find_all_in_season() == [user_point_2021]
            assert UserPoint.find_all_in_season(2022) == []
