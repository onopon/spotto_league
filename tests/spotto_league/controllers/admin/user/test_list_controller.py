from tests.spotto_league.controllers.base_controller import BaseController
from tests.modules.data_creator import DataCreator


class TestListController(BaseController):
    def test_get_access_as_admin(self):
        user = DataCreator().create('admin_user')
        self.login(user.login_name, 'password')
        url_path = '/admin/user/list'
        result = self.get(url_path)
        assert result.status_code == 200
        assert url_path in result.url

    def test_get_access_as_member(self):
        user = DataCreator().create('member_user')
        self.login(user.login_name, 'password')
        url_path = '/admin/user/list'
        result = self.get(url_path)
        assert result.status_code == 401
        assert url_path in result.url

    def test_get_access_as_visitor(self):
        user = DataCreator().create('visitor_user')
        self.login(user.login_name, 'password')
        url_path = '/admin/user/list'
        result = self.get(url_path)
        assert result.status_code == 401
        assert url_path in result.url

    def test_get_access_as_not_login(self):
        url_path = '/admin/user/list'
        result = self.get(url_path)
        assert result.status_code == 200
        assert '/user/login' in result.url
