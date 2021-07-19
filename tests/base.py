import pytest
import spotto_league.models
import application
from spotto_league.database import db

app = application.app


class Base(object):
    @pytest.fixture(scope="function", autouse=True)
    def pre_function(self):
        with app.app_context():
            self.set_up()
            yield
            self.tear_down()

    # overrideする時は
    # super().set_up()
    # を呼び出すこと
    def set_up(self):
        # DB全消去（※ local環境でテストを実行する場合、idはincrementされたままなので注意）
        for m in spotto_league.models.all():
            m.query.delete()
        db.session.commit()

    # overrideする時は
    # super().tear_down()
    # を呼び出すこと
    def tear_down(self):
        db.session.close()
