import os
from spotto_league.database import init_db
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # 標準設定ファイル読み込み
    app.config.from_object("settings")

    # 非公開設定ファイル読み込み
    app.config.from_pyfile(os.path.join("config", "common.py"), silent=True)
    if app.config["ENV"] == "development":
        app.config.from_pyfile(os.path.join("config", "development.py"), silent=True)
    else:
        app.config.from_pyfile(os.path.join("config", "production.py"), silent=True)

    init_db(app)
    app.secret_key = app.config["SECRET_KEY"]
    return app
