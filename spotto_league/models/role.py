from typing import Optional
from datetime import datetime
from spotto_league.database import db
from spotto_league.modules.password_util import PasswordUtil
import hashlib
import flask_login
from typing import Dict, Any
from spotto_league.database import SpottoDB
from .base import Base


class Role(db.Model, Base):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    role_type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
