import os
from spotto_league.database import init_db
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from spotto_league.database import SpottoDB

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

app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# https://github.com/miguelgrinberg/Flask-Migrate/issues/50#issuecomment-79080496
# dbが作られた後にmodelをimportしないと、migrateの対象となってくれない
import spotto_league.models

if __name__ == '__main__':
    manager.run()
