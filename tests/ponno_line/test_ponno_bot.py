from ponno_line.ponno_bot import PonnoBot
from tests.base import Base
from tests.modules.ponno_line_decorator import PonnoLineDecorator
from tests.modules.data_creator import DataCreator
import freezegun


class TestPonnoBot(Base):
    decorator = PonnoLineDecorator()

    def _push_about_birthday(self):
        user = DataCreator().create('admin_user')
        with freezegun.freeze_time('2021-{}-{} 00:00:00'.format(user.birthday.month, user.birthday.day)):
            PonnoBot.push_about_birthday()

    @decorator.line_pushed
    def test_push_about_birthday(self):
        self._push_about_birthday()

    @decorator.notify_posted
    def test_push_about_birthday_notify_posted(self):
        self._push_about_birthday()

    @decorator.line_not_pushed
    def test_push_about_birthday_not_called(self):
        user = DataCreator().create('admin_user')
        # guestとvisitorは誕生日でも祝ってもらえない
        DataCreator().create('guest_user', {'birthday': '1990-{}-{}'.format(user.birthday.month, user.birthday.day)})
        DataCreator().create('visitor_user', {'birthday': '1992-{}-{}'.format(user.birthday.month, user.birthday.day)})

        with freezegun.freeze_time('2021-{}-{} 00:00:00'.format(user.birthday.month, user.birthday.day + 1)):
            PonnoBot.push_about_birthday()

    def _push_about_unpaid(self):
        user = DataCreator().create('member_user')
        user.unpaid.amount = 1000
        user.unpaid.save()
        PonnoBot.push_about_unpaid()

    @decorator.line_pushed
    def test_push_about_unpaid(self):
        self._push_about_unpaid()

    @decorator.notify_posted
    def test_push_about_unpaid_notify_posted(self):
        self._push_about_unpaid()

    @decorator.line_not_pushed
    def test_push_about_unpaid_not_called(self):
        # 未払いのユーザが0人
        PonnoBot.push_about_unpaid()
