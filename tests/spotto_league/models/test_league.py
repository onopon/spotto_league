from spotto_league.scripts.add_league_point import AddLeaguePoint
from spotto_league.models.league import League, LeagueStatus
from spotto_league.models.league_point import LeaguePoint
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_log import LeagueLog
from tests.base import Base
from tests.modules.data_creator import DataCreator
import freezegun
import datetime


class TestLeague(Base):
    def test_properties(self, monkeypatch):
        AddLeaguePoint().execute()
        user = DataCreator().create('guest_user')
        user_2 = DataCreator().create('member_user')
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', {'place_id': place.id})
        lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, user.id)
        lm.save()
        lm_enabled = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, user_2.id)
        lm_enabled.enabled = True
        lm_enabled.save()
        league_log = LeagueLog.find_or_initialize(league.id, user.id, user_2.id)
        league_log.save()

        # coverrage 対策で2回やってる
        assert league.place == place
        assert league.place == place
        assert league.members == [lm, lm_enabled]
        assert league.enable_members == [lm_enabled]
        # coverrage 対策で2回やってる
        assert league.logs == [league_log]
        assert league.logs == [league_log]
        assert league.start_datetime == datetime.datetime(2021, 6, 25, 17, 0)
        assert league.date_for_display == '06月25日（金）17:00 - 21:00'
        assert league.time_for_display == '17:00 - 21:00'
        assert league.join_end_at_for_display == '06月24日（木）20:00'

        assert league.recommend_league_point_group_id == LeaguePoint.BASE_GROUP_ID
        with monkeypatch.context() as m:
            m.setattr(LeaguePoint, 'RATING_BORDER_MEMBER_COUNT', len(league.enable_members))
            league = League.find_by_id(league.id)
            assert league.recommend_league_point_group_id == LeaguePoint.ONE_AND_HALF_TIMES_GROUP_ID

        assert league.league_points == []
        league.league_point_group_id = 1
        league_points = LeaguePoint.find_all_by_group_id(1)
        # coverrage 対策で2回やってる
        assert league.league_points == league_points
        assert league.league_points == league_points

    def test_statuses(self):
        league = DataCreator().create('default_league', {'place_id': 1})
        assert league.is_status_recruiting()
        assert not league.is_status_ready()
        assert not league.is_status_finished()
        assert not league.is_status_cancel()
        assert not league.is_status_recruiting_near_join_end_at()

        league.ready()
        assert league.is_status_ready()
        assert not league.is_status_recruiting()
        assert league.is_status_ready()
        assert not league.is_status_finished()
        assert not league.is_status_cancel()
        assert not league.is_status_recruiting_near_join_end_at()

        league.finish()
        assert not league.is_status_ready()
        assert not league.is_status_recruiting()
        assert not league.is_status_ready()
        assert league.is_status_finished()
        assert not league.is_status_cancel()
        assert not league.is_status_recruiting_near_join_end_at()

        league.cancel()
        assert not league.is_status_ready()
        assert not league.is_status_recruiting()
        assert not league.is_status_ready()
        assert league.is_status_finished()
        assert league.is_status_cancel()
        assert not league.is_status_recruiting_near_join_end_at()

        league.recruiting_near_join_end_at()
        assert not league.is_status_ready()
        assert league.is_status_recruiting()
        assert not league.is_status_ready()
        assert not league.is_status_finished()
        assert not league.is_status_cancel()
        assert league.is_status_recruiting_near_join_end_at()

    def test_league_point_group_id_is(self):
        league = DataCreator().create('default_league', {'place_id': 1})
        assert league.league_point_group_id_is(LeaguePoint.BASE_GROUP_ID)
        assert not league.league_point_group_id_is(LeaguePoint.ONE_AND_HALF_TIMES_GROUP_ID)

    def test_user(self):
        user = DataCreator().create('guest_user')
        lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(1, user.id)
        # coverrage 対策で2回やってる
        assert lm.user == user
        assert lm.user == user

    def test_find_all_by_league_id(self):
        league_id = 1
        expects = []
        lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(league_id, 1)
        lm.save()
        expects.append(lm)

        lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(league_id, 2)
        lm.save()
        expects.append(lm)

        # 検索に引っかからないデータ
        lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(league_id + 1, 1)
        lm.save()

        assert LeagueMember.find_all_by_league_id(league_id) == expects

    def test_find_all_by_user_id(self):
        user_id = 1
        expects = []
        lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(1, user_id)
        lm.save()
        expects.append(lm)

        # 検索に引っかからないデータ
        lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(1, user_id + 1)
        lm.save()

        lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(2, user_id)
        lm.save()
        expects.append(lm)

        assert LeagueMember.find_all_by_user_id(user_id) == expects

    def test_find_limit_all_enabled_by_user_id(self):
        user_id = 1
        expects = []
        with freezegun.freeze_time('2021-07-28 00:00:00'):
            # 検索には引っかかるがlimitで足切られるデータ
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(1, user_id)
            lm.enabled = True
            lm.save()

            # 検索に引っかからないデータ
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(1, 2)
            lm.enabled = True
            lm.save()

        with freezegun.freeze_time('2021-07-29 00:00:00'):
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(2, user_id)
            lm.enabled = True
            lm.save()
            expects.append(lm)

            # 検索に引っかからないデータ
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(2, 3)
            lm.save()

        with freezegun.freeze_time('2021-07-30 00:00:00'):
            # 検索に引っかからないデータ
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(3, user_id)
            lm.save()

        with freezegun.freeze_time('2021-07-31 00:00:00'):
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(4, user_id)
            lm.enabled = True
            lm.save()
            expects.append(lm)

        expects.reverse()
        count = 2
        results = LeagueMember.find_limit_all_enabled_by_user_id(user_id, count)
        assert results == expects

    def test_is_on_today(self):
        league = DataCreator().create('default_league', {'place_id': 1, 'date': '2021-08-03'})
        with freezegun.freeze_time('2021-08-02 23:59:59'):
            assert not league.is_on_today()

        with freezegun.freeze_time('2021-08-03 00:00:00'):
            assert league.is_on_today()

        with freezegun.freeze_time('2021-08-03 23:59:59'):
            assert league.is_on_today()

        with freezegun.freeze_time('2021-08-04 00:00:00'):
            assert not league.is_on_today()

    def test_all(self):
        league = DataCreator().create('default_league', {'place_id': 1, 'date': '2021-08-03'})
        result = League.all()
        assert result == [league]

    def test_find_all_for_cosecutive_win_bonus_point(self):
        league = DataCreator().create('default_league', {'place_id': 1, 'date': '2021-08-17'})
        league.league_point_group_id = 1
        league.finish()
        league.save()
        with freezegun.freeze_time('2021-08-17 23:59:59'):
            assert not League.find_all_for_cosecutive_win_bonus_point()

        with freezegun.freeze_time('2021-08-18 00:00:00'):
            assert not League.find_all_for_cosecutive_win_bonus_point()

        with freezegun.freeze_time('2022-01-08 00:00:00'):
            assert not League.find_all_for_cosecutive_win_bonus_point()

        league = DataCreator().create('default_league', {'place_id': 1, 'date': '2021-08-18'})
        with freezegun.freeze_time('2021-08-18 00:00:00'):
            assert not League.find_all_for_cosecutive_win_bonus_point()

        with freezegun.freeze_time('2022-01-08 00:00:00'):
            assert not League.find_all_for_cosecutive_win_bonus_point()
        league.league_point_group_id = 1
        league.finish()
        league.save()
        with freezegun.freeze_time('2021-08-18 00:00:00'):
            assert League.find_all_for_cosecutive_win_bonus_point() == [league]
        with freezegun.freeze_time('2022-01-08 00:00:00'):
            assert not League.find_all_for_cosecutive_win_bonus_point() == [league]

        league_2 = DataCreator().create('default_league', {'place_id': 1, 'date': '2022-01-01'})
        with freezegun.freeze_time('2022-01-08 00:00:00'):
            assert not League.find_all_for_cosecutive_win_bonus_point()
        league_2.league_point_group_id = 1
        league_2.finish()
        league_2.save()
        with freezegun.freeze_time('2022-01-08 00:00:00'):
            assert League.find_all_for_cosecutive_win_bonus_point() == [league_2]

        # created_atとdateの順番が交差してしまっている場合
        with freezegun.freeze_time('2022-02-01 00:00:00'):
            league_3 = DataCreator().create('default_league', {'place_id': 1, 'date': '2022-02-08', 'start_at': '18:00:00'})
            league_3.league_point_group_id = 1
            league_3.finish()
            league_3.save()
        with freezegun.freeze_time('2022-02-02 00:00:00'):
            league_4 = DataCreator().create('default_league', {'place_id': 1, 'date': '2022-02-09'})
            league_4.league_point_group_id = 1
            league_4.finish()
            league_4.save()
        with freezegun.freeze_time('2022-02-03 00:00:00'):
            league_5 = DataCreator().create('default_league', {'place_id': 1, 'date': '2022-02-07'})
            league_5.league_point_group_id = 1
            league_5.finish()
            league_5.save()
        with freezegun.freeze_time('2022-02-03 00:00:00'):
            league_6 = DataCreator().create('default_league', {'place_id': 1, 'date': '2022-02-08', 'start_at': '10:00:00'})
            league_6.league_point_group_id = 1
            league_6.finish()
            league_6.save()
        with freezegun.freeze_time('2022-02-10 00:00:00'):
            assert League.find_all_for_cosecutive_win_bonus_point() == [league_4, league_3, league_6, league_5, league_2]

    def test_is_in_join_session(self):
        league = DataCreator().create('default_league', {'place_id': 1, 'date': '2021-08-06', 'join_end_at': '2021-08-05 23:59:59'})
        with freezegun.freeze_time('2021-08-05 23:59:58'):
            assert league.is_in_join_session()
        with freezegun.freeze_time('2021-08-05 23:59:59'):
            assert not league.is_in_join_session()

    def test_is_stopped_recruiting(self):
        league = DataCreator().create('default_league', {'place_id': 1, 'date': '2021-08-06', 'join_end_at': '2021-08-05 23:59:59'})
        with freezegun.freeze_time('2021-08-05 23:59:59'):
            assert not league.is_stopped_recruiting()
            league.status = LeagueStatus.READY.value
            assert league.is_stopped_recruiting()
        with freezegun.freeze_time('2021-08-06 00:00:00'):
            league.status = LeagueStatus.RECRUITING.value
            assert league.is_stopped_recruiting()
            league.status = LeagueStatus.READY.value
            assert league.is_stopped_recruiting()

    def test_session(self):
        league = DataCreator().create('default_league',
                                      {'place_id': 1,
                                       'date': '2021-08-06',
                                       'start_at': '18:00:00',
                                       'end_at': '21:00:00',
                                       'join_end_at': '2021-08-05 23:59:59'})
        with freezegun.freeze_time('2021-08-06 17:59:59'):
            assert league.is_before_session()
            assert not league.is_in_session()
            assert not league.is_after_session()

        with freezegun.freeze_time('2021-08-06 18:00:00'):
            assert not league.is_before_session()
            assert league.is_in_session()
            assert not league.is_after_session()

        with freezegun.freeze_time('2021-08-06 21:00:00'):
            assert not league.is_before_session()
            assert league.is_in_session()
            assert not league.is_after_session()

        with freezegun.freeze_time('2021-08-06 21:00:01'):
            assert not league.is_before_session()
            assert not league.is_in_session()
            assert league.is_after_session()

    def test_is_near_join_end_at(self):
        league = DataCreator().create('default_league', {'place_id': 1, 'date': '2021-08-06', 'join_end_at': '2021-08-05 23:00:00'})

        with freezegun.freeze_time('2021-08-04 20:00:00'):
            assert not league.is_near_join_end_at()
            league.status = LeagueStatus.READY.value
            assert not league.is_near_join_end_at()

        with freezegun.freeze_time('2021-08-05 19:59:59'):
            league.status = LeagueStatus.RECRUITING.value
            assert not league.is_near_join_end_at()
            league.status = LeagueStatus.READY.value
            assert not league.is_near_join_end_at()

        with freezegun.freeze_time('2021-08-05 20:00:00'):
            league.status = LeagueStatus.RECRUITING.value
            assert league.is_near_join_end_at()
            league.status = LeagueStatus.READY.value
            assert not league.is_near_join_end_at()

        with freezegun.freeze_time('2021-08-05 20:00:01'):
            league.status = LeagueStatus.RECRUITING.value
            assert league.is_near_join_end_at()
            league.status = LeagueStatus.READY.value
            assert not league.is_near_join_end_at()

        with freezegun.freeze_time('2021-08-06 20:00:00'):
            league.status = LeagueStatus.RECRUITING.value
            assert not league.is_near_join_end_at()
            league.status = LeagueStatus.READY.value
            assert not league.is_near_join_end_at()
