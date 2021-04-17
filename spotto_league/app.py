import os
from spotto_league.database import init_db
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # 標準設定ファイル読み込み
    app.config.from_object("settings")
    environment = os.environ.get('ENV', app.config["DEFAULT_ENV"])
    secret_key = os.environ.get('SECRET_KEY', app.config["DEFAULT_SECRET_KEY"]).encode('utf-8')

    # 非公開設定ファイル読み込み
    app.config.from_pyfile(os.path.join("config", "common.py"), silent=True)
    if environment == "development":
        app.config.from_pyfile(os.path.join("config", "development.py"), silent=True)
    else:
        app.config.from_pyfile(os.path.join("config", "production.py"), silent=True)

    init_db(app)
    app.secret_key = secret_key
    return app
