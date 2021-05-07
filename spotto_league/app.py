import os
from spotto_league.database import init_db
import locale
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


def create_app():
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    app = Flask(__name__, instance_relative_config=True)
    # 標準設定ファイル読み込み
    app.config.from_object("settings")
    environment = app.config['ENV']
    secret_key = app.config['SECRET_KEY'].encode('utf-8')

    # 非公開設定ファイル読み込み
    app.config.from_pyfile(os.path.join("config", "db.py"), silent=True)

    init_db(app)
    app.secret_key = secret_key
    return app
