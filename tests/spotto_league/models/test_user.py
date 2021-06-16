from spotto_league.models.user import User
from spotto_league.modules.password_util import PasswordUtil

def test_set_password():
    user = User()
    password = "password"
    user.set_password(password)
    assert user.password == PasswordUtil.make_hex(password)
    assert False
