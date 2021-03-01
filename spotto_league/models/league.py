from datetime import datetime
from flask_sample.database import db


class League(db.Model):

    __tablename__ = 'leagues'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.now().date)
    name = db.Column(db.String(255), nullable=False)
    game_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
