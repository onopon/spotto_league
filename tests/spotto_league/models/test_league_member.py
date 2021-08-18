from spotto_league.models.user import User, Gender
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.role import Role
from spotto_league.modules.password_util import PasswordUtil
from tests.base import Base
from tests.modules.data_creator import DataCreator
import datetime
import freezegun


class TestLeagueMember(Base):
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

    def test_find_or_initialize_by_league_id_and_user_id(self):
        league_id = 1
        user_id = 2
        lm = LeagueMember.find_or_initialize_by_league_id_and_user_id(league_id, user_id)
        assert lm.id is None
        assert lm.user_id == user_id
        assert lm.league_id == league_id
        lm.save()
        assert lm.id is not None

        lm_2 = LeagueMember.find_or_initialize_by_league_id_and_user_id(league_id, user_id)
        assert lm.id == lm_2.id
