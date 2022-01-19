from tests.spotto_league.controllers.base_controller import BaseController
from tests.modules.data_creator import DataCreator
from spotto_league.models.role import RoleType
from spotto_league.models.unpaid import Unpaid

URL_PATH = '/admin/user/list'


class TestPostListController(BaseController):
    def test_post_as_admin(self):
        user = DataCreator().create('admin_user')
        user.unpaid.amount = 1000
        user.unpaid.memo = "事前に作成したけど消えるメモ"
        user.unpaid.save()
        self.login(user.login_name, 'password')

        user_2 = DataCreator().create('member_user')
        user_3 = DataCreator().create('guest_user')
        # visitorは含まれない
        DataCreator().create('visitor_user')

        args = {"radio_{}".format(user.login_name): RoleType.ADMIN.value,
                "radio_{}".format(user_2.login_name): RoleType.GUEST.value,
                "radio_{}".format(user_3.login_name): RoleType.MEMBER.value,
                "unpaid_{}".format(user.login_name): 0,
                "unpaid_{}".format(user_2.login_name): 1000,
                "unpaid_{}".format(user_3.login_name): 0,
                "unpaid_memo_{}".format(user.login_name): "",
                "unpaid_memo_{}".format(user_2.login_name): "このメモは残る",
                "unpaid_memo_{}".format(user_3.login_name): "このメモは消える"}
        result = self.post(URL_PATH, args)
        assert result.status_code == 200
        assert user.is_admin()
        assert user_2.is_guest()
        assert user_3.is_member()
        assert not Unpaid.find_or_initialize_by_user_id(user.id).id
        assert user_2.unpaid.amount == 1000
        assert user_2.unpaid.memo == "このメモは残る"
        assert not user_3.unpaid.memo

    def test_post_cannot_change_role_if_user_not_setting_name(self):
        user = DataCreator().create('admin_user')
        self.login(user.login_name, 'password')
        guest_user = DataCreator().create('guest_user')
        guest_user.last_name = ""
        guest_user.first_name = ""
        guest_user.save()

        for role_type_value in [RoleType.ADMIN.value, RoleType.MEMBER.value]:
            args = {"radio_{}".format(user.login_name): RoleType.ADMIN.value,
                    "radio_{}".format(guest_user.login_name): role_type_value,
                    "unpaid_{}".format(user.login_name): 0,
                    "unpaid_{}".format(guest_user.login_name): 0,
                    "unpaid_memo_{}".format(user.login_name): "",
                    "unpaid_memo_{}".format(guest_user.login_name): ""}
            result = self.post(URL_PATH, args)
            assert result.status_code == 200
            assert guest_user.is_guest()

    def test_post_can_change_to_withdrawaler_if_user_not_setting_name(self):
        user = DataCreator().create('admin_user')
        self.login(user.login_name, 'password')
        guest_user = DataCreator().create('guest_user')
        guest_user.last_name = ""
        guest_user.first_name = ""
        guest_user.save()

        args = {"radio_{}".format(user.login_name): RoleType.ADMIN.value,
                "radio_{}".format(guest_user.login_name): RoleType.WITHDRAWALER.value,
                "unpaid_{}".format(user.login_name): 0,
                "unpaid_{}".format(guest_user.login_name): 0,
                "unpaid_memo_{}".format(user.login_name): "",
                "unpaid_memo_{}".format(guest_user.login_name): ""}
        result = self.post(URL_PATH, args)
        assert result.status_code == 200
        assert guest_user.is_withdrawaler()

    def test_post_cannot_change_role_myself(self):
        user = DataCreator().create('admin_user')
        self.login(user.login_name, 'password')
        args = {"radio_{}".format(user.login_name): RoleType.MEMBER.value,
                "unpaid_{}".format(user.login_name): 0,
                "unpaid_memo_{}".format(user.login_name): ""}
        result = self.post(URL_PATH, args)
        assert result.status_code == 200
        assert user.is_admin()

    def test_post_as_member(self):
        user = DataCreator().create('member_user')
        self.login(user.login_name, 'password')
        url_path = '/admin/user/list'
        result = self.get(url_path)
        args = {"radio_{}".format(user.login_name): RoleType.ADMIN.value,
                "unpaid_{}".format(user.login_name): 0,
                "unpaid_memo_{}".format(user.login_name): ""}
        result = self.post(URL_PATH, args)
        assert result.status_code == 200
        assert user.is_member()

    def test_post_as_visitor(self):
        user = DataCreator().create('visitor_user')
        self.login(user.login_name, 'password')
        args = {"radio_{}".format(user.login_name): RoleType.ADMIN.value,
                "unpaid_{}".format(user.login_name): 0,
                "unpaid_memo_{}".format(user.login_name): ""}
        result = self.post(URL_PATH, args)
        assert result.status_code == 200
        assert user.is_visitor()

    def test_post_as_withdrawaler(self):
        user = DataCreator().create('withdrawaler_user')
        self.login(user.login_name, 'password')
        args = {"radio_{}".format(user.login_name): RoleType.ADMIN.value,
                "unpaid_{}".format(user.login_name): 0,
                "unpaid_memo_{}".format(user.login_name): ""}
        result = self.post(URL_PATH, args)
        assert result.status_code == 200
        assert user.is_withdrawaler()

    def test_post_as_not_login(self):
        user = DataCreator().create('admin_user')
        args = {"radio_{}".format(user.login_name): RoleType.ADMIN.value,
                "unpaid_{}".format(user.login_name): 0,
                "unpaid_memo_{}".format(user.login_name): ""}
        result = self.post(URL_PATH, args)
        assert result.status_code == 302
        assert '/user/login' in result.headers.get('Location')
