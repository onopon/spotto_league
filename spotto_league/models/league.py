from datetime import datetime
from spotto_league.database import db
from datetime import datetime as dt
from typing import List
from spotto_league.database import SpottoDB
from spotto_league.models.league_log import LeagueLog


class League(db.Model):

    __tablename__ = 'leagues'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.now().date, index=True)
    name = db.Column(db.String(255), nullable=False)
    game_count = db.Column(db.Integer, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @property
    def logs(self) -> List[LeagueLog]:
        return SpottoDB().session.query(LeagueLog).\
                filter_by(league_id=self.id).all()
