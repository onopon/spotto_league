from tests.base import Base
from spotto_league.modules.password_util import PasswordUtil
from instance import settings


class TestPasswordUtil(Base):
    def test_make_hex(self):
        password = 'password'
        password_hex = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'
        assert PasswordUtil.make_hex(password) == password_hex

    def test_is_same(self):
        password = 'password'
        password_hex = PasswordUtil.make_hex(password)
        assert PasswordUtil.is_same(password, password_hex)
        wrong_password = 'hoge'
        assert not PasswordUtil.is_same(wrong_password, password_hex)

    def test_is_correct_common_password(self):
        password = settings.COMMON_PASSWORD
        assert PasswordUtil.is_correct_common_password(password)
        assert not PasswordUtil.is_correct_common_password(password + 'hoge')
        assert not PasswordUtil.is_correct_common_password(settings.COMMON_VISITOR_PASSWORD)

    def test_is_correct_common_visitor_password(self):
        password = settings.COMMON_VISITOR_PASSWORD
        assert PasswordUtil.is_correct_common_visitor_password(password)
        assert not PasswordUtil.is_correct_common_visitor_password(password + 'hoge')
        assert not PasswordUtil.is_correct_common_visitor_password(settings.COMMON_PASSWORD)
