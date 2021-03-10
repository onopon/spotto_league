from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate

db = SQLAlchemy()

# SQLAlchemyをシングルトンにする
class SpottoDB(SQLAlchemy):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(SpottoDB, cls).__new__(cls)
        return cls._instance

def init_db(app):
    SpottoDB().init_app(app)
    Migrate(app, SpottoDB())

def make_session_for_debug():
    import os
    from flask import Flask
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("settings")
    app.config.from_pyfile(os.path.join("config", "common.py"), silent=True)
    app.config.from_pyfile(os.path.join("config", "development.py"), silent=True)
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    SessionClass = sessionmaker(engine)
    session = SessionClass()
    return session
