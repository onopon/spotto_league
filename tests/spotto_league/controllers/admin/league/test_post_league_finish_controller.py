from tests.spotto_league.controllers.base_controller import BaseController
from tests.modules.data_creator import DataCreator
from spotto_league.controllers.admin.league.post_league_finish_controller import INVALID_MATCH_GROUP_ID
from spotto_league.scripts.add_league_point import AddLeaguePoint
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league import LeagueStatus
from spotto_league.models.bonus_point import BonusPoint
from spotto_league.entities.point_rank import PointRank
from spotto_league.entities.continuous_point import ContinuousPoint

URL_PATH = '/admin/league/{}/finish'


class TestPostLeagueFinishController(BaseController):
    def test_normal(self, mocker):
        AddLeaguePoint().execute()
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id, 'status': LeagueStatus.READY.value})

        admin_user = DataCreator().create('admin_user')
        users = DataCreator().create('six_member_users')
        guest = DataCreator().create('guest_user')
        visitor = DataCreator().create('visitor_user')
        users.append(guest)
        users.append(visitor)
        b_point = 1500
        bonus_point = BonusPoint.find_or_initialize_by_user_id(users[1].id)
        bonus_point.point = b_point
        bonus_point.available_count = 4
        bonus_point.save()
        for u in users:
            league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, u.id)
            league_member.enabled = True
            league_member.save()
        user = users[2]
        league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, user.id)

        league_log_2 = LeagueLog.find_or_initialize(league.id, users[1].id, users[2].id)
        league_log_2.save()

        # users[2]を基準として見ているので、
        # users[0] vs users[2] は 2-0でusers[0]の勝ちとなる
        log_details_hash = {0: 'league_log_details_2_0',
                            1: 'league_log_details_1_2',
                            3: 'league_log_details_0_2',
                            4: 'league_log_details_2_1',
                            5: None}
        for (index, yml_title) in log_details_hash.items():
            league_log = LeagueLog.find_or_initialize(league.id, user.id, users[index].id)
            league_log.save()
            if yml_title:
                DataCreator().create(yml_title, overrided_dict={'league_log_id': league_log.id})

        self.login(admin_user.login_name, 'password')
        assert league.league_point_group_id is None

        # 連勝記録
        mocker.patch.object(ContinuousPoint, 'count_for_bonus', 3)

        result = self.post(URL_PATH.format(league.id), {"league_point_group_id": 1})
        assert result.status_code == 302
        point_ranks = PointRank.make_point_rank_list(league)
        expected_hash_list = [
            {'user_id': users[2].id, 'Total': 6000, 'LeaguePoint': [3000], 'BonusPoint': 1500, 'ContinuousPoint': 1500},
            {'user_id': users[0].id, 'Total': 2000, 'LeaguePoint': [2000], 'BonusPoint': 0, 'ContinuousPoint': 0},
            {'user_id': users[3].id, 'Total': 1500, 'LeaguePoint': [1500], 'BonusPoint': 0, 'ContinuousPoint': 0},
            {'user_id': users[5].id, 'Total': 1200, 'LeaguePoint': [1200], 'BonusPoint': 0, 'ContinuousPoint': 0},
            {'user_id': users[4].id, 'Total': 800, 'LeaguePoint': [800], 'BonusPoint': 0, 'ContinuousPoint': 0},
            {'user_id': users[1].id, 'Total': 700, 'LeaguePoint': [700], 'BonusPoint': 0, 'ContinuousPoint': 0},
            {'user_id': admin_user.id, 'Total': 0, 'LeaguePoint': [], 'BonusPoint': 0, 'ContinuousPoint': 0},
            {'user_id': guest.id, 'Total': 0, 'LeaguePoint': [], 'BonusPoint': 0, 'ContinuousPoint': 0},
        ]
        for i, point_rank in enumerate(point_ranks):
            expected_hash = expected_hash_list[i]
            assert point_rank.user.id == expected_hash['user_id']
            assert point_rank.current_point == expected_hash['Total']
            assert point_rank.current_league_points == expected_hash['LeaguePoint']
            assert point_rank.current_league_points == expected_hash['LeaguePoint']
            assert point_rank.current_league_points == expected_hash['LeaguePoint']
            assert point_rank.current_bonus_point == expected_hash['BonusPoint']
            assert point_rank.current_bonus_point == expected_hash['ContinuousPoint']
        assert league.league_point_group_id == 1
        assert LeagueStatus(league.status) == LeagueStatus.FINISHED

    def test_invalid_group_id(self):
        AddLeaguePoint().execute()
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id, 'status': LeagueStatus.READY.value})

        admin_user = DataCreator().create('admin_user')
        users = DataCreator().create('six_member_users')
        guest = DataCreator().create('guest_user')
        visitor = DataCreator().create('visitor_user')
        users.append(guest)
        users.append(visitor)
        b_point = 1500
        bonus_point = BonusPoint.find_or_initialize_by_user_id(users[1].id)
        bonus_point.point = b_point
        bonus_point.available_count = 4
        bonus_point.save()
        for u in users:
            league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, u.id)
            league_member.enabled = True
            league_member.save()
        user = users[2]
        league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, user.id)

        league_log_2 = LeagueLog.find_or_initialize(league.id, users[1].id, users[2].id)
        league_log_2.save()

        # users[2]を基準として見ているので、
        # users[0] vs users[2] は 2-0でusers[0]の勝ちとなる
        log_details_hash = {0: 'league_log_details_2_0',
                            1: 'league_log_details_1_2',
                            3: 'league_log_details_0_2',
                            4: 'league_log_details_2_1',
                            5: None}
        for (index, yml_title) in log_details_hash.items():
            league_log = LeagueLog.find_or_initialize(league.id, user.id, users[index].id)
            league_log.save()
            if yml_title:
                DataCreator().create(yml_title, overrided_dict={'league_log_id': league_log.id})

        self.login(admin_user.login_name, 'password')
        assert league.league_point_group_id is None
        result = self.post(URL_PATH.format(league.id), {"league_point_group_id": INVALID_MATCH_GROUP_ID})
        assert result.status_code == 302
        point_ranks = PointRank.make_point_rank_list(league)
        expected_hash_list = [
            {'user_id': admin_user.id, 'LeaguePoint': [], 'BonusPoint': 0},
            {'user_id': users[0].id, 'LeaguePoint': [0], 'BonusPoint': 0},
            {'user_id': users[1].id, 'LeaguePoint': [0], 'BonusPoint': 0},
            {'user_id': users[2].id, 'LeaguePoint': [0], 'BonusPoint': 0},
            {'user_id': users[3].id, 'LeaguePoint': [0], 'BonusPoint': 0},
            {'user_id': users[4].id, 'LeaguePoint': [0], 'BonusPoint': 0},
            {'user_id': users[5].id, 'LeaguePoint': [0], 'BonusPoint': 0},
            {'user_id': guest.id, 'LeaguePoint': [], 'BonusPoint': 0},
        ]
        for i, point_rank in enumerate(point_ranks):
            print(point_rank.user.name)
            expected_hash = expected_hash_list[i]
            assert point_rank.user.id == expected_hash['user_id']
            assert point_rank.current_league_points == expected_hash['LeaguePoint']
            assert point_rank.current_league_points == expected_hash['LeaguePoint']
            assert point_rank.current_bonus_point == expected_hash['BonusPoint']
        assert league.league_point_group_id == INVALID_MATCH_GROUP_ID
        assert LeagueStatus(league.status) == LeagueStatus.FINISHED

    def test_invalidate(self):
        user = DataCreator().create('admin_user')
        self.login(user.login_name, 'password')
        result = self.post(URL_PATH.format(0), {"league_point_group_id": 0})
        assert result.status_code == 404

        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id})
        result = self.post(URL_PATH.format(league.id), {"league_point_group_id": 0})
        assert result.status_code == 404

        league.ready()
        league.save()
        result = self.post(URL_PATH.format(league.id))
        assert result.status_code == 404

        league.finish()
        league.save()
        result = self.post(URL_PATH.format(league.id), {"league_point_group_id": 0})
        assert result.status_code == 404
