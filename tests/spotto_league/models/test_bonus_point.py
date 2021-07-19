from spotto_league.models.bonus_point import BonusPoint
from tests.base import Base
from tests.modules.data_creator import DataCreator


class TestBonusPoint(Base):
    def test_all(self):
        users = DataCreator().create('two_member_users')
        bonus_points = []
        for user in users:
            bonus_point = BonusPoint()
            bonus_point.user_id = user.id
            bonus_point.point = 1500
            bonus_point.available_count = 10
            bonus_point.save()
            bonus_points.append(bonus_point)
        assert BonusPoint.all() == bonus_points

    def test_find_by_user_id(self):
        user_id = 1
        bonus_point = BonusPoint()
        bonus_point.user_id = user_id
        bonus_point.point = 1500
        bonus_point.available_count = 10
        bonus_point.save()
        assert BonusPoint.find_by_user_id(user_id) == bonus_point
        assert BonusPoint.find_by_user_id(user_id + 1) is None

    def test_find_or_initialize_by_user_id(self):
        user_id = 1
        bonus_point = BonusPoint()
        bonus_point.user_id = user_id
        bonus_point.point = 1500
        bonus_point.available_count = 10
        bonus_point.save()

        result = BonusPoint.find_or_initialize_by_user_id(user_id)
        assert result == bonus_point
        result = BonusPoint.find_or_initialize_by_user_id(user_id + 1)
        assert result.id is None
        assert result.user_id == user_id + 1

    def test_find_all_by_user_ids(self):
        users = DataCreator().create('two_member_users')
        bonus_points = []
        for user in users:
            bonus_point = BonusPoint()
            bonus_point.user_id = user.id
            bonus_point.point = 1500
            bonus_point.available_count = 10
            bonus_point.save()
            bonus_points.append(bonus_point)
        user_ids = [user.id for user in users]
        user_ids.append(users[1].id + 1)  # テスト用にdummyのデータを混ぜる
        assert BonusPoint.find_all_by_user_ids(user_ids) == bonus_points

    def test_user(self):
        user = DataCreator().create('member_user')
        bonus_point = BonusPoint.find_or_initialize_by_user_id(user.id)
        bonus_point.point = 1500
        bonus_point.available_count = 10
        bonus_point.save()
        assert bonus_point.user == user
        # coverage 対応
        assert bonus_point.user == user
