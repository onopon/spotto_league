from ponno_line.ponno_bot import PonnoBot
from tests.base import Base
from tests.modules.ponno_line_decorator import PonnoLineDecorator
from tests.modules.data_creator import DataCreator
from spotto_league.models.league import League, LeagueStatus
from spotto_league.models.league_member import LeagueMember
import freezegun
from datetime import timedelta


class TestPonnoBot(Base):
    decorator = PonnoLineDecorator()

    def _push_about_birthday(self):
        user = DataCreator().create('admin_user')
        with freezegun.freeze_time('2021-{}-{} 00:00:00'.format(user.birthday.month, user.birthday.day)):
            PonnoBot.push_about_birthday()

    def _create_league_and_some_users(self) -> League:
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id, 'status': LeagueStatus.READY.value})
        admin_user = DataCreator().create('admin_user')
        guest = DataCreator().create('guest_user')
        users = [admin_user, guest]
        for u in users:
            league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, u.id)
            league_member.enabled = True
            league_member.save()
        return league

    @decorator.line_pushed
    def test_push_about_birthday(self):
        self._push_about_birthday()

    @decorator.line_pushed
    def test_push_about_league_day_before(self):
        league = self._create_league_and_some_users()
        with freezegun.freeze_time('{} 00:00:00'.format(league.date - timedelta(days=1))):
            PonnoBot.push_about_league_day_before()

    @decorator.line_not_pushed
    def test_push_about_league_day_before_not_called(self):
        league = self._create_league_and_some_users()
        with freezegun.freeze_time('{} 00:00:00'.format(league.date)):
            PonnoBot.push_about_league_day_before()

    @decorator.notify_posted
    def test_push_about_league_day_before_notify_posted(self):
        league = self._create_league_and_some_users()
        with freezegun.freeze_time('{} 00:00:00'.format(league.date - timedelta(days=1))):
            PonnoBot.push_about_league_day_before()

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
