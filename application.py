import os
from flask import Flask, request, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from spotto_league.database import init_db
import spotto_league.models
from spotto_league.database import db
from datetime import date
from spotto_league.controllers.league_list_controller import LeagueListController
from spotto_league.controllers.league_controller import LeagueController


auth = HTTPBasicAuth()


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
    return app

app = create_app()

@auth.verify_password
def verify_password(username, password):
    if username == app.config["BASIC_USER"] and\
        check_password_hash(generate_password_hash(app.config["BASIC_PASS"]), password):
        return username

@app.route("/", methods=("GET", "POST"))
@auth.login_required
def league_list():
    return LeagueListController(db.session).render(request)

@app.route("/league/<int:league_id>/", methods=("GET", "POST"))
@auth.login_required
def league(league_id: int):
    return LeagueController(db.session).render(request, league_id=league_id)

def init_data_for_debug():
    league = spotto_league.models.league.League()
    league.name = '第1回まぐカップ'
    league.date = date(2021, 2, 1)
    league.game_count = 3
    db.session.add(league)

    league = spotto_league.models.league.League()
    league.name = '第2回まぐカップ'
    league.date = date(2021, 2, 8)
    league.game_count = 5
    db.session.add(league)

    user = spotto_league.models.user.User()
    user.login_name = 'magu'
    user.password = 'password'
    user.name = 'まぐ'
    db.session.add(user)

    user = spotto_league.models.user.User()
    user.login_name = 'uchida'
    user.password = 'password'
    user.name = 'うっちー'
    db.session.add(user)

    user = spotto_league.models.user.User()
    user.login_name = 'watako'
    user.password = 'password'
    user.name = 'わたこう'
    db.session.add(user)

    user = spotto_league.models.user.User()
    user.login_name = 'yukinori'
    user.password = 'password'
    user.name = 'ゆっきー'
    db.session.add(user)

    user = spotto_league.models.user.User()
    user.login_name = 'onopon'
    user.password = 'password'
    user.name = 'おのぽん'
    db.session.add(user)

    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 1
    league_member.user_id = 1
    db.session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 1
    league_member.user_id = 4
    db.session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 1
    league_member.user_id = 2
    league_member.enabled = False
    db.session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 1
    league_member.user_id = 5
    db.session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 1
    league_member.user_id = 3
    db.session.add(league_member)

    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 2
    league_member.user_id = 1
    db.session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 2
    league_member.user_id = 2
    db.session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 2
    league_member.user_id = 4
    db.session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 2
    league_member.user_id = 5
    db.session.add(league_member)

    league_log = spotto_league.models.league_log.LeagueLog()
    league_log.league_id = 1
    league_log.user_id_1 = 3
    league_log.user_id_2 = 4
    db.session.add(league_log)
    league_log = spotto_league.models.league_log.LeagueLog()
    league_log.league_id = 1
    league_log.user_id_1 = 1
    league_log.user_id_2 = 5
    db.session.add(league_log)

    league_log = spotto_league.models.league_log.LeagueLog()
    league_log.league_id = 2
    league_log.user_id_1 = 2
    league_log.user_id_2 = 5
    db.session.add(league_log)

    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 1
    league_log_detail.score_1 = 11
    league_log_detail.score_2 = 9
    db.session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 1
    league_log_detail.score_1 = 11
    league_log_detail.score_2 = 5
    db.session.add(league_log_detail)

    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 2
    league_log_detail.score_1 = 12
    league_log_detail.score_2 = 10
    db.session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 2
    league_log_detail.score_1 = 8
    league_log_detail.score_2 = 11
    db.session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 15
    league_log_detail.score_2 = 13
    db.session.add(league_log_detail)

    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 11
    league_log_detail.score_2 = 3
    db.session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 11
    league_log_detail.score_2 = 2
    db.session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 10
    league_log_detail.score_2 = 12
    db.session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 8
    league_log_detail.score_2 = 11
    db.session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 11
    league_log_detail.score_2 = 4
    db.session.add(league_log_detail)

    db.session.commit()
