import os
import flask_login
from flask import Flask, request, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from spotto_league.database import init_db
import spotto_league.models
from spotto_league.database import SpottoDB
from datetime import date
from spotto_league.controllers.league_list_controller import LeagueListController
from spotto_league.controllers.league_controller import LeagueController
from spotto_league.controllers.user.register_controller import RegisterController as UserRegisterController
from spotto_league.controllers.user.post_register_controller import PostRegisterController as PostUserRegisterController
from spotto_league.controllers.user.login_controller import LoginController as UserLoginController
from spotto_league.controllers.user.post_login_controller import PostLoginController as PostUserLoginController
from spotto_league.modules.password_util import PasswordUtil
from spotto_league.models.user import User

auth = HTTPBasicAuth()
login_manager = flask_login.LoginManager()


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
    login_manager.init_app(app)
    login_manager.login_view = 'user_login'
    return app

app = create_app()

@auth.verify_password
def verify_password(username, password):
    if username == app.config["BASIC_USER"] and\
        check_password_hash(generate_password_hash(app.config["BASIC_PASS"]), password):
        return username

@app.route("/", methods=("GET", "POST"))
@auth.login_required
@flask_login.login_required
def league_list():
    return LeagueListController().render(request)

@app.route("/league/<int:league_id>/", methods=("GET", "POST"))
@auth.login_required
@flask_login.login_required
def league(league_id: int):
    return LeagueController().render(request, league_id=league_id)

@app.route("/league/<int:league_id>/json", methods=("GET", "POST"))
@auth.login_required
@flask_login.login_required
def league_json_data(league_id: int):
    return LeagueController().render_as_json(request, league_id=league_id)

@app.route("/user/register", methods=("GET", "POST"))
@auth.login_required
def user_register():
    if request.method == "POST":
        return PostUserRegisterController().render(request)
    return UserRegisterController().render(request)

@app.route("/user/login", methods=("GET", "POST"))
@auth.login_required
@login_manager.unauthorized_handler
def user_login():
    if request.method == "POST":
        return PostUserLoginController().render(request)
    return UserLoginController().render(request)

@app.route("/user/logout", methods=("GET", "POST"))
@auth.login_required
@login_manager.unauthorized_handler
def user_logout():
    flask_login.logout_user()
    return redirect(url_for('user_login'))

'''
for flask-login
'''
@login_manager.user_loader
def user_loader(login_name):
    name_tuples = SpottoDB().session.query(User.login_name).all()
    login_names = [t[0] for t in name_tuples]
    if login_name not in login_names:
        return

    user = User()
    user.login_name = login_name
    user.id = login_name
    return user

'''
for flask-login
'''
@login_manager.request_loader
def request_loader(request):
    name_tuples = SpottoDB().session.query(User.login_name).all()
    login_names = [t[0] for t in name_tuples]
 
    login_name = request.form.get('login_name')
    if login_name not in login_names:
        return

    user = User()
    user.login_name = login_name
    user.id = login_name
    flask_login.login_user(user)
    return user


def init_data_for_debug():
    league = spotto_league.models.league.League()
    league.name = '第1回まぐカップ'
    league.date = date(2021, 2, 1)
    league.game_count = 3
    SpottoDB().session.add(league)

    league = spotto_league.models.league.League()
    league.name = '第2回まぐカップ'
    league.date = date(2021, 2, 8)
    league.game_count = 5
    SpottoDB().session.add(league)

    user = spotto_league.models.user.User()
    user.login_name = 'magu'
    user.password = 'password'
    user.name = 'まぐ'
    SpottoDB().session.add(user)

    user = spotto_league.models.user.User()
    user.login_name = 'uchida'
    user.password = 'password'
    user.name = 'うっちー'
    SpottoDB().session.add(user)

    user = spotto_league.models.user.User()
    user.login_name = 'watako'
    user.password = 'password'
    user.name = 'わたこう'
    SpottoDB().session.add(user)

    user = spotto_league.models.user.User()
    user.login_name = 'yukinori'
    user.password = 'password'
    user.name = 'ゆっきー'
    SpottoDB().session.add(user)

    user = spotto_league.models.user.User()
    user.login_name = 'onopon'
    user.password = 'password'
    user.name = 'おのぽん'
    SpottoDB().session.add(user)

    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 1
    league_member.user_id = 1
    SpottoDB().session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 1
    league_member.user_id = 4
    SpottoDB().session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 1
    league_member.user_id = 2
    league_member.enabled = False
    SpottoDB().session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 1
    league_member.user_id = 5
    SpottoDB().session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 1
    league_member.user_id = 3
    SpottoDB().session.add(league_member)

    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 2
    league_member.user_id = 1
    SpottoDB().session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 2
    league_member.user_id = 2
    SpottoDB().session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 2
    league_member.user_id = 4
    SpottoDB().session.add(league_member)
    league_member = spotto_league.models.league_member.LeagueMember()
    league_member.league_id = 2
    league_member.user_id = 5
    SpottoDB().session.add(league_member)

    league_log = spotto_league.models.league_log.LeagueLog()
    league_log.league_id = 1
    league_log.user_id_1 = 3
    league_log.user_id_2 = 4
    SpottoDB().session.add(league_log)
    league_log = spotto_league.models.league_log.LeagueLog()
    league_log.league_id = 1
    league_log.user_id_1 = 1
    league_log.user_id_2 = 5
    SpottoDB().session.add(league_log)

    league_log = spotto_league.models.league_log.LeagueLog()
    league_log.league_id = 2
    league_log.user_id_1 = 2
    league_log.user_id_2 = 5
    SpottoDB().session.add(league_log)

    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 1
    league_log_detail.score_1 = 11
    league_log_detail.score_2 = 9
    SpottoDB().session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 1
    league_log_detail.score_1 = 11
    league_log_detail.score_2 = 5
    SpottoDB().session.add(league_log_detail)

    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 2
    league_log_detail.score_1 = 12
    league_log_detail.score_2 = 10
    SpottoDB().session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 2
    league_log_detail.score_1 = 8
    league_log_detail.score_2 = 11
    SpottoDB().session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 15
    league_log_detail.score_2 = 13
    SpottoDB().session.add(league_log_detail)

    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 11
    league_log_detail.score_2 = 3
    SpottoDB().session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 11
    league_log_detail.score_2 = 2
    SpottoDB().session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 10
    league_log_detail.score_2 = 12
    SpottoDB().session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 8
    league_log_detail.score_2 = 11
    SpottoDB().session.add(league_log_detail)
    league_log_detail = spotto_league.models.league_log_detail.LeagueLogDetail()
    league_log_detail.league_log_id = 3
    league_log_detail.score_1 = 11
    league_log_detail.score_2 = 4
    SpottoDB().session.add(league_log_detail)

    SpottoDB().session.commit()
