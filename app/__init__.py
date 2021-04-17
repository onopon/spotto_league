import os
import locale
import flask_login
from flask import Flask, request, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from spotto_league.database import init_db
from spotto_league.database import db
from datetime import date
from spotto_league.controllers.league_list_controller import LeagueListController
from spotto_league.controllers.league_controller import LeagueController
from spotto_league.controllers.user.exists_controller import ExistsController as UserExistsController
from spotto_league.controllers.user.register_controller import RegisterController as UserRegisterController
from spotto_league.controllers.user.post_register_controller import PostRegisterController as PostUserRegisterController
from spotto_league.controllers.user.login_controller import LoginController as UserLoginController
from spotto_league.controllers.user.post_login_controller import PostLoginController as PostUserLoginController
from spotto_league.controllers.user.info_controller import InfoController as UserInfoController
from spotto_league.controllers.user.modify_controller import ModifyController as UserModifyController
from spotto_league.controllers.user.modify_password_controller import ModifyPasswordController as UserModifyPasswordController
from spotto_league.controllers.user.post_modify_controller import PostModifyController as PostUserModifyController
from spotto_league.controllers.user.post_modify_password_controller import PostModifyPasswordController as PostUserModifyPasswordController
from spotto_league.controllers.post_league_log_controller import PostLeagueLogController as PostLeagueLogController
from spotto_league.controllers.admin.league.register_controller import RegisterController as AdminLeagueRegisterController
from spotto_league.controllers.admin.league.post_register_controller import PostRegisterController as PostAdminLeagueRegisterController
from spotto_league.controllers.admin.league.league_controller import LeagueController as AdminLeagueController
from spotto_league.controllers.admin.league.post_league_controller import PostLeagueController as PostAdminLeagueController
from spotto_league.controllers.admin.league.post_league_finish_controller import PostLeagueFinishController as PostAdminLeagueFinishController
from spotto_league.controllers.user.post_league_join_controller import PostLeagueJoinController as PostUserLeagueJoinController
from spotto_league.controllers.user.post_league_cancel_controller import PostLeagueCancelController as PostUserLeagueCancelController
from spotto_league.modules.password_util import PasswordUtil
from spotto_league.models.user import User

auth = HTTPBasicAuth()
login_manager = flask_login.LoginManager()


def create_app():
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
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
    login_manager.init_app(app)
    login_manager.login_view = 'user_login'
    return app

app = create_app()

@auth.verify_password
def verify_password(username, password):
    basic_user = os.environ.get('BASIC_USER', app.config["DEFAULT_BASIC_USER"])
    basic_pass = os.environ.get('BASIC_PASS', app.config["DEFAULT_SECRET_KEY"])
    if username == basic_user and\
        check_password_hash(generate_password_hash(basic_pass), password):
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

@app.route("/league/log", methods=("GET", "POST"))
@auth.login_required
@flask_login.login_required
def league_log():
    if request.method == "POST":
        return PostLeagueLogController().render(request)

@app.route("/user/register", methods=("GET", "POST"))
@auth.login_required
def user_register():
    if request.method == "POST":
        return PostUserRegisterController().render(request)
    return UserRegisterController().render(request)

@app.route("/user/<string:login_name>/exists", methods=("GET", "POST"))
@auth.login_required
def user_exists(login_name: str):
    return UserExistsController().render(request, login_name=login_name)

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

@app.route("/user/info/<string:login_name>/", methods=("GET", "POST"))
@auth.login_required
@flask_login.login_required
def user_info(login_name: str):
    return UserInfoController().render(request, login_name=login_name)

@app.route("/user/modify/", methods=("GET", "POST"))
@auth.login_required
@flask_login.login_required
def user_modify():
    if request.method == "POST":
        return PostUserModifyController().render(request)
    return UserModifyController().render(request)

@app.route("/user/modify/password/", methods=("GET", "POST"))
@auth.login_required
@flask_login.login_required
def user_modify_password():
    if request.method == "POST":
        return PostUserModifyPasswordController().render(request)
    return UserModifyPasswordController().render(request)

@app.route("/user/league/join", methods=("GET", "POST"))
def user_league_join():
    if request.method == "POST":
        return PostUserLeagueJoinController().render(request)

@app.route("/user/league/cancel", methods=("GET", "POST"))
def user_league_cancel():
    if request.method == "POST":
        return PostUserLeagueCancelController().render(request)

@app.route("/admin/league/register/", methods=("GET", "POST"))
@auth.login_required
@flask_login.login_required
def admin_league_register():
    if request.method == "POST":
        return PostAdminLeagueRegisterController().render(request)
    return AdminLeagueRegisterController().render(request)

@app.route("/admin/league/<int:league_id>/", methods=("GET", "POST"))
@auth.login_required
@flask_login.login_required
def admin_league(league_id: int):
    if request.method == "POST":
        return PostAdminLeagueController().render(request, league_id=league_id)
    return AdminLeagueController().render(request, league_id=league_id)

@app.route("/admin/league/<int:league_id>/finish", methods=("GET", "POST"))
@auth.login_required
@flask_login.login_required
def admin_league_finish(league_id: int):
    if request.method == "POST":
        return PostAdminLeagueFinishController().render(request, league_id=league_id)

'''
for flask-login
'''
@login_manager.user_loader
def user_loader(login_name):
    name_tuples = db.session.query(User.login_name).all()
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
    name_tuples = db.session.query(User.login_name).all()
    login_names = [t[0] for t in name_tuples]
 
    login_name = request.form.get('login_name')
    if login_name not in login_names:
        return

    user = User()
    user.login_name = login_name
    user.id = login_name
    flask_login.login_user(user)
    return user