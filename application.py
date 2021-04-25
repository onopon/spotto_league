import os
import locale
import flask_login
from flask import Flask, request, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.pool import Pool
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
from spotto_league.controllers.user.ranking_controller import RankingController as UserRankingController
from spotto_league.controllers.post_league_log_controller import PostLeagueLogController as PostLeagueLogController
from spotto_league.controllers.admin.league.register_controller import RegisterController as AdminLeagueRegisterController
from spotto_league.controllers.admin.league.modify_controller import ModifyController as AdminLeagueModifyController
from spotto_league.controllers.admin.league.post_register_controller import PostRegisterController as PostAdminLeagueRegisterController
from spotto_league.controllers.admin.league.league_controller import LeagueController as AdminLeagueController
from spotto_league.controllers.admin.league.post_league_controller import PostLeagueController as PostAdminLeagueController
from spotto_league.controllers.admin.league.post_league_finish_controller import PostLeagueFinishController as PostAdminLeagueFinishController
from spotto_league.controllers.admin.user.register_point_controller import RegisterPointController as AdminUserRegisterPointController
from spotto_league.controllers.admin.user.post_register_point_controller import PostRegisterPointController as PostAdminUserRegisterPointController
from spotto_league.controllers.admin.user.list_controller import ListController as AdminUserListController
from spotto_league.controllers.admin.user.post_list_controller import PostListController as PostAdminUserListController
from spotto_league.controllers.user.post_league_join_controller import PostLeagueJoinController as PostUserLeagueJoinController
from spotto_league.controllers.user.post_league_cancel_controller import PostLeagueCancelController as PostUserLeagueCancelController
from spotto_league.modules.password_util import PasswordUtil
from spotto_league.models.user import User

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

@app.route("/", methods=("GET", "POST"))
@flask_login.login_required
def league_list():
    return LeagueListController().render(request)

@app.route("/league/<int:league_id>/", methods=("GET", "POST"))
@flask_login.login_required
def league(league_id: int):
    if request.method == "POST":
        if int(request.form.get("status_join", 0)):
            PostUserLeagueJoinController().render(request)
        else:
            PostUserLeagueCancelController().render(request)
    return LeagueController().render(request, league_id=league_id)

@app.route("/league/<int:league_id>/json", methods=("GET", "POST"))
@flask_login.login_required
def league_json_data(league_id: int):
    return LeagueController().render_as_json(request, league_id=league_id)

@app.route("/league/log", methods=("GET", "POST"))
@flask_login.login_required
def league_log():
    if request.method == "POST":
        return PostLeagueLogController().render(request)

@app.route("/user/register", methods=("GET", "POST"))
def user_register():
    if request.method == "POST":
        return PostUserRegisterController().render(request)
    return UserRegisterController().render(request)

@app.route("/user/<string:login_name>/exists", methods=("GET", "POST"))
def user_exists(login_name: str):
    return UserExistsController().render(request, login_name=login_name)

@app.route("/user/login", methods=("GET", "POST"))
@login_manager.unauthorized_handler
def user_login():
    if request.method == "POST":
        return PostUserLoginController().render(request)
    return UserLoginController().render(request)

@app.route("/user/logout", methods=("GET", "POST"))
@login_manager.unauthorized_handler
def user_logout():
    flask_login.logout_user()
    return redirect(url_for('user_login'))

@app.route("/user/info/<string:login_name>/", methods=("GET", "POST"))
@flask_login.login_required
def user_info(login_name: str):
    return UserInfoController().render(request, login_name=login_name)

@app.route("/user/modify/", methods=("GET", "POST"))
@flask_login.login_required
def user_modify():
    if request.method == "POST":
        return PostUserModifyController().render(request)
    return UserModifyController().render(request)

@app.route("/user/modify/password/", methods=("GET", "POST"))
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

@app.route("/user/ranking/<int:year>/", methods=("GET", "POST"))
def user_ranking(year: int):
    return UserRankingController().render(request, year=year)

@app.route("/user/ranking/<int:year>/json", methods=("GET", "POST"))
@flask_login.login_required
def user_ranking_json_data(year: int):
    return UserRankingController().render_as_json(request, year=year)

@app.route("/admin/league/register/", methods=("GET", "POST"))
@flask_login.login_required
def admin_league_register():
    if request.method == "POST":
        return PostAdminLeagueRegisterController().render(request)
    return AdminLeagueRegisterController().render(request)

@app.route("/admin/league/modify/", methods=("GET", "POST"))
@flask_login.login_required
def admin_league_modify():
    if request.method == "POST":
        return PostAdminLeagueRegisterController().render(request)
    return AdminLeagueModifyController().render(request)

@app.route("/admin/league/<int:league_id>/", methods=("GET", "POST"))
@flask_login.login_required
def admin_league(league_id: int):
    if request.method == "POST":
        return PostAdminLeagueController().render(request, league_id=league_id)
    return AdminLeagueController().render(request, league_id=league_id)

@app.route("/admin/league/<int:league_id>/finish", methods=("GET", "POST"))
@flask_login.login_required
def admin_league_finish(league_id: int):
    if request.method == "POST":
        return PostAdminLeagueFinishController().render(request, league_id=league_id)

@app.route("/admin/user/register/point", methods=("GET", "POST"))
@flask_login.login_required
def admin_user_register_point():
    if request.method == "POST":
        return PostAdminUserRegisterPointController().render(request)
    return AdminUserRegisterPointController().render(request)

@app.route("/admin/user/list", methods=("GET", "POST"))
@flask_login.login_required
def admin_user_list():
    if request.method == "POST":
        return PostAdminUserListController().render(request)
    return AdminUserListController().render(request)

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

'''
for SqlAlchemy on production
https://qiita.com/yukiB/items/67336716b242df3be350
'''
# @event.listens_for(Pool, "checkout")
# def ping_connection(dbapi_connection, connection_record, connection_proxy):
#     cursor = dbapi_connection.cursor()
#     try:
#         cursor.execute("SELECT 1")
#     except:
#         raise exc.DisconnectionError()
#     cursor.close()
