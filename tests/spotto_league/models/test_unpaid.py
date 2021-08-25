from spotto_league.models.unpaid import Unpaid
from tests.base import Base
from tests.modules.data_creator import DataCreator


class TestUnpaid(Base):
    def test_all(self):
        unpaid = Unpaid()
        unpaid.user_id = 1
        unpaid.amount = 3000
        unpaid.save()
        unpaid_2 = Unpaid()
        unpaid_2.user_id = 2
        unpaid_2.amount = 5000
        unpaid_2.save()
        assert Unpaid.all() == [unpaid, unpaid_2]
