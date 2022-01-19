from instance import settings
from tests.spotto_league.controllers.base_controller import BaseController
from tests.modules.data_creator import DataCreator


class TestPostLoginController(BaseController):
    def test_post_as_success(self):
        dc = DataCreator()
        users = [dc.create('admin_user'), dc.create('guest_user'), dc.create('member_user')]
        for user in users:
            args = {'login_name': user.login_name,
                    'password': 'password',
                    'common_password': settings.COMMON_PASSWORD}
            result = self.post("/user/login", data=args)
            assert result.status_code == 302
            assert 'http://127.0.0.1/' in result.headers.get('Location')
            self.logout()

        visitor_user = dc.create('visitor_user')
        args = {'login_name': visitor_user.login_name,
                'password': 'password',
                'common_password': settings.COMMON_VISITOR_PASSWORD}
        result = self.post("/user/login", data=args)
        assert result.status_code == 302
        assert 'http://127.0.0.1/' in result.headers.get('Location')

    def test_post_as_failed(self):
        dc = DataCreator()
        visitor_user = dc.create('visitor_user')

        users = [dc.create('admin_user'), dc.create('guest_user'), dc.create('member_user'), dc.create('withdrawaler_user')]
        for user in users:
            args = {'login_name': user.login_name,
                    'password': 'INVALID_password',
                    'common_password': settings.COMMON_PASSWORD}
            result = self.post("/user/login", data=args)
            assert result.status_code == 200
            assert 'login-error' in str(result.data)

            args = {'login_name': user.login_name,
                    'password': 'password',
                    'common_password': settings.COMMON_VISITOR_PASSWORD}
            result = self.post("/user/login", data=args)
            assert result.status_code == 200
            assert 'login-error' in str(result.data)

        args = {'login_name': visitor_user.login_name,
                'password': 'invalid_password',
                'common_password': settings.COMMON_VISITOR_PASSWORD}
        result = self.post("/user/login", data=args)
        assert result.status_code == 200
        assert 'login-error' in str(result.data)
