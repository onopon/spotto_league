from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from spotto_league.app import create_app
from datetime import datetime
from spotto_league.database import db

app = create_app()
migrate = Migrate(app, db)

# https://github.com/miguelgrinberg/Flask-Migrate/issues/50#issuecomment-79080496
# dbが作られた後にmodelをimportしないと、migrateの対象となってくれない
import spotto_league.models

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
