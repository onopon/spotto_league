from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league import LeagueStatus
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail
from spotto_league.modules.league_settlement_calculator import LeagueSettlementCalculator
from spotto_league.scripts.add_league_point import AddLeaguePoint
from spotto_league.entities.continuous_point import ContinuousPoint
from tests.base import Base
from tests.modules.data_creator import DataCreator
import freezegun


class TestContinuousPoint(Base):
    def test_calcurate_continuous_count(self):
        AddLeaguePoint().execute()
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id, 'date': '2021-08-18', 'status': LeagueStatus.FINISHED.value, 'league_point_group_id': 1})
        league_2 = DataCreator().create('default_league', overrided_dict={'place_id': place.id, 'date': '2021-08-19', 'league_point_group_id': 1})
        users = DataCreator().create('six_member_users')
        for u in users:
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, u.id)
            lm.enabled = True
            lm.save()
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(league_2.id, u.id)
            lm.enabled = True
            lm.save()
        continuous_point = ContinuousPoint(users[0].id, league.id)
        assert continuous_point._calcurate_continuous_count() == 0
        continuous_point = ContinuousPoint(users[0].id, league_2.id)
        assert continuous_point._calcurate_continuous_count() == 1
        for i in range(1, len(users) - 1):
            user = users[i]
            continuous_point = ContinuousPoint(user.id, league.id)
            assert continuous_point._calcurate_continuous_count() == 0
            continuous_point = ContinuousPoint(user.id, league_2.id)
            assert continuous_point._calcurate_continuous_count() == 0

        league_2.finish()
        league_2.save()
        continuous_point = ContinuousPoint(users[0].id, league_2.id + 1)
        assert continuous_point._calcurate_continuous_count() == 2
        for i in range(1, len(users) - 1):
            user = users[i]
            continuous_point = ContinuousPoint(user.id, league_2.id + 1)
            assert continuous_point._calcurate_continuous_count() == 0

    def test_some_properties(self):
        user = DataCreator().create('member_user')
        continuous_point = ContinuousPoint(user.id, 1)
        for count in range(0, ContinuousPoint.LIMIT_COUNT_FOR_CONTINUOUS_BONUS):
            continuous_point._continuous_count = count
            assert continuous_point.count_for_bonus == count
            assert continuous_point.count_for_display == count + 1
            assert continuous_point.point == ContinuousPoint.CONTINUOUS_POINT_BASE * count

        for count in range(ContinuousPoint.LIMIT_COUNT_FOR_CONTINUOUS_BONUS, (ContinuousPoint.LIMIT_COUNT_FOR_CONTINUOUS_BONUS * 2 - 1)):
            continuous_point._continuous_count = count
            assert continuous_point.count_for_bonus == count - ContinuousPoint.LIMIT_COUNT_FOR_CONTINUOUS_BONUS
            assert continuous_point.count_for_display == count + 1
            assert continuous_point.point == ContinuousPoint.CONTINUOUS_POINT_BASE * (count - ContinuousPoint.LIMIT_COUNT_FOR_CONTINUOUS_BONUS)
