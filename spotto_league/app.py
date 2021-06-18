from spotto_league.database import init_db
import locale
from flask import Flask


def create_app():
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    app = Flask(__name__, instance_relative_config=True)
    # 非公開設定ファイル読み込み
    app.config.from_pyfile("settings.py", silent=True)
    # 標準設定ファイル読み込み
    app.config.from_object("config")
    secret_key = app.config["SECRET_KEY"].encode("utf-8")

    init_db(app)
    app.secret_key = secret_key
    return app
