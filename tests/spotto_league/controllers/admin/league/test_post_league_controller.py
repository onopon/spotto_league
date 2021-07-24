from tests.spotto_league.controllers.base_controller import BaseController
from tests.modules.data_creator import DataCreator
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league import LeagueStatus

URL_PATH = '/admin/league/{}/'


class TestPostLeagueController(BaseController):
    def test_normal_and_override(self):
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id, 'status': LeagueStatus.READY.value})

        admin = DataCreator().create('admin_user')
        two_members = DataCreator().create('two_member_users')
        guest = DataCreator().create('guest_user')
        visitor = DataCreator().create('visitor_user')

        users = [admin, two_members[0], two_members[1], guest, visitor]
        enabled_league_member_ids = []
        enabled_league_member_ids_2 = []
        for user in users:
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, user.id)
            lm.save()
            enabled_league_member_ids.append(lm.id)
            enabled_league_member_ids_2.append(lm.id)
        enabled_league_member_ids.pop(2)
        enabled_league_member_ids_2.pop(-1)

        self.login(admin.login_name, 'password')
        assert not any([m.enabled for m in league.members])
        result = self.post(URL_PATH.format(league.id), {"enabled_league_member_ids": enabled_league_member_ids})
        assert result.status_code == 302
        for user in users:
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, user.id)
            if user.id == two_members[1].id:
                assert not lm.enabled
            else:
                assert lm.enabled
        assert LeagueStatus(league.status) == LeagueStatus.READY

        # league_member更新
        result = self.post(URL_PATH.format(league.id), {"enabled_league_member_ids": enabled_league_member_ids_2})
        assert result.status_code == 302
        for user in users:
            lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, user.id)
            if user.id == visitor.id:
                assert not lm.enabled
            else:
                assert lm.enabled
        assert LeagueStatus(league.status) == LeagueStatus.READY

    def test_invalidate(self):
        user = DataCreator().create('admin_user')
        self.login(user.login_name, 'password')
        result = self.post(URL_PATH.format(0), {"enabled_league_member_ids": []})
        assert result.status_code == 404

        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id})
        league.finish()
        league.save()
        result = self.post(URL_PATH.format(league.id), {"enabled_league_member_ids": []})
        assert result.status_code == 404

        league.cancel()
        league.save()
        result = self.post(URL_PATH.format(league.id), {"enabled_league_member_ids": []})
        assert result.status_code == 404

        league.status = LeagueStatus.RECRUITING.value
        league.save()
        result = self.post(URL_PATH.format(league.id))
        assert result.status_code == 404

        result = self.post(URL_PATH.format(league.id), {"enabled_league_member_ids": [1]})
        assert result.status_code == 404
