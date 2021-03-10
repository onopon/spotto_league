from datetime import datetime
from spotto_league.database import db
from spotto_league.database import SpottoDB


class Base():
    def save(self):
        session = SpottoDB().session
        session.add(self)
        session.commit()
