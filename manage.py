from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from spotto_league.app import create_app

app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# https://github.com/miguelgrinberg/Flask-Migrate/issues/50#issuecomment-79080496
# dbが作られた後にmodelをimportしないと、migrateの対象となってくれない
import spotto_league.models

if __name__ == '__main__':
    manager.run()
