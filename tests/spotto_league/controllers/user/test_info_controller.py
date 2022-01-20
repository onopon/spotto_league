from tests.spotto_league.controllers.base_controller import BaseController
from tests.modules.data_creator import DataCreator
from spotto_league.models.role import RoleType


class TestInfoController(BaseController):
    def test_get_as_success(self):
        dc = DataCreator()
        users = [dc.create('admin_user'), dc.create('guest_user'), dc.create('member_user')]
        for login_user in users:
            self.login(login_user.login_name, 'password')
            for user in users:
                result = self.get("/user/info/{}/".format(user.login_name))
                assert result.status_code == 200
            self.logout()

    def test_get_as_not_login(self):
        dc = DataCreator()
        users = [dc.create('admin_user'), dc.create('guest_user'), dc.create('member_user')]
        for user in users:
            result = self.get("/user/info/{}/".format(user.login_name))
            assert result.status_code == 302
            assert '/user/login' in result.headers.get('Location')

    def test_get_to_does_not_exist_user(self):
        dc = DataCreator()
        user = dc.create('admin_user')
        self.login(user.login_name, 'password')
        result = self.get("/user/info/{}/".format("do_not_exist_user"))
        assert result.status_code == 404

    def test_get_to_visitor_user(self):
        dc = DataCreator()
        user = dc.create('admin_user')
        self.login(user.login_name, 'password')
        visitor_user = dc.create('visitor_user')
        result = self.get("/user/info/{}/".format(visitor_user.login_name))
        assert result.status_code == 404

    def test_get_to_withdrawaler_user(self):
        dc = DataCreator()
        user = dc.create('admin_user')
        self.login(user.login_name, 'password')
        withdrawaler_user = dc.create('withdrawaler_user')
        result = self.get("/user/info/{}/".format(withdrawaler_user.login_name))
        assert result.status_code == 404

    def test_get_to_member_but_exchange_to_withdrawaler_myself(self):
        dc = DataCreator()
        user = dc.create('member_user')
        self.login(user.login_name, 'password')
        result = self.get("/user/info/{}/".format(user.login_name))
        assert result.status_code == 200

        user.role.role_type = RoleType.WITHDRAWALER.value
        user.role.save()

        result = self.get("/user/info/{}/".format(user.login_name))
        assert result.status_code == 302
        assert '/user/login' in result.headers['Location']
