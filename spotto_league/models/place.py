from datetime import datetime
from typing import List
from spotto_league.database import db
from .base import Base


class Place(db.Model, Base):

    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255))
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def all(cls) -> List['Place']:
        return db.session.query(cls).all()
