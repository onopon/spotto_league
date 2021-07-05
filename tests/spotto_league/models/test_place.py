from tests.base import Base
from tests.modules.data_creator import DataCreator
from spotto_league.models.place import Place


class TestPlace(Base):
    def test_all(self):
        place = DataCreator().create('place')
        place_2 = DataCreator().create('place')
        result = Place.all()
        assert result == [place, place_2]
