from spotto_league.models.user import User, Gender
from spotto_league.models.role import Role
from spotto_league.modules.password_util import PasswordUtil
from tests.base import Base
from tests.modules.test_data_creator import TestDataCreator
import datetime
import freezegun


class TestUser(Base):
    def test_set_password(self):
        user = User()
        password = "password"
        user.set_password(password)
        assert user.password == PasswordUtil.make_hex(password)

    def test_all(self):
        data = TestDataCreator().create('two_guest_users')
        assert User.all() == data

    def test_all_without_visitor(self):
        users_without_visitor = []
        users_without_visitor.append(TestDataCreator().create('guest_user'))
        users_without_visitor.append(TestDataCreator().create('admin_user'))
        users_without_visitor.append(TestDataCreator().create('member_user'))
        TestDataCreator().create('visitor_user')
        assert User.all_without_visitor() == users_without_visitor

    def test_find_by_login_name(self):
        user = TestDataCreator().create('guest_user')
        assert not User.find_by_login_name('hogehoge')
        assert User.find_by_login_name(user.login_name) == user

    def test_to_hash(self):
        user = TestDataCreator().create('guest_user')
        target = user.to_hash()
        assert target['id'] == user.id
        assert target['login_name'] == user.login_name
        assert target['name'] == user.name

    def test_role(self):
        user = TestDataCreator().create('guest_user')
        assert type(user.role) == Role
        # coverage 対応
        assert type(user.role) == Role

    def test_is_admin(self):
        assert not TestDataCreator().create('guest_user').is_admin()
        assert TestDataCreator().create('admin_user').is_admin()
        assert not TestDataCreator().create('member_user').is_admin()
        assert not TestDataCreator().create('visitor_user').is_admin()

    def test_is_member(self):
        assert not TestDataCreator().create('guest_user').is_member()
        assert not TestDataCreator().create('admin_user').is_member()
        assert TestDataCreator().create('member_user').is_member()
        assert not TestDataCreator().create('visitor_user').is_member()

    def test_is_guest(self):
        assert TestDataCreator().create('guest_user').is_guest()
        assert not TestDataCreator().create('admin_user').is_guest()
        assert not TestDataCreator().create('member_user').is_guest()
        assert not TestDataCreator().create('visitor_user').is_guest()

    def test_is_visitor(self):
        assert not TestDataCreator().create('guest_user').is_visitor()
        assert not TestDataCreator().create('admin_user').is_visitor()
        assert not TestDataCreator().create('member_user').is_visitor()
        assert TestDataCreator().create('visitor_user').is_visitor()

    def test_birthday_for_display(self):
        user = User()
        user.birthday = datetime.date(1989, 9, 3)
        assert user.birthday_for_display == "09月03日"

    def test_age(self):
        user = User()
        user.birthday = datetime.date(1989, 9, 3)
        with freezegun.freeze_time('2021-09-02 23:59:59'):
            assert user.age == 31

        with freezegun.freeze_time('2021-09-03 00:00:00'):
            assert user.age == 32

    def test_gender_for_display(self):
        user = User()
        user.gender = Gender.MALE
        assert user.gender_for_display == "男性"
        user.gender = Gender.FEMALE
        assert user.gender_for_display == "女性"
        user.gender = 3
        assert user.gender_for_display == ""
