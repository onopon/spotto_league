import os
import traceback
import locale
import flask_login
from flask import Flask, request, render_template, redirect, url_for, abort
from datetime import datetime as dt
from linebot import (
    WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from spotto_league.database import init_db
from spotto_league.database import db
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
from spotto_league.controllers.admin.league.post_league_finish_controller import (
    PostLeagueFinishController as PostAdminLeagueFinishController
)
from spotto_league.controllers.admin.league.league_cancel_controller import LeagueCancelController as AdminLeagueCancelController
from spotto_league.controllers.admin.league.post_notify_recruiting_controller import (
    PostNotifyRecruitingController as PostAdminLeagueNotifyRecruitingController
)
from spotto_league.controllers.admin.user.register_point_controller import RegisterPointController as AdminUserRegisterPointController
from spotto_league.controllers.admin.user.post_register_point_controller import (
    PostRegisterPointController as PostAdminUserRegisterPointController
)
from spotto_league.controllers.admin.user.list_controller import ListController as AdminUserListController
from spotto_league.controllers.admin.user.post_list_controller import PostListController as PostAdminUserListController
from spotto_league.controllers.user.post_league_join_controller import PostLeagueJoinController as PostUserLeagueJoinController
from spotto_league.controllers.user.post_league_cancel_controller import PostLeagueCancelController as PostUserLeagueCancelController
from spotto_league.models.user import User
from ponno_line.ponno_notify import PonnoNotify


login_manager = flask_login.LoginManager()


def create_app():
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    app = Flask(__name__, instance_relative_config=True)
    '''
    下記Warning 対策( https://stackoverflow.com/questions/67521860/jinja2-deprecationwarning-the-autoescape-extension-is-deprecated-and-will-b )
    /usr/local/lib/python3.7/site-packages/jinja2/environment.py:362: DeprecationWarning: The 'autoescape' extension is deprecated and will be removed in Jinja 3.1. This is built in now.  # noqa
    /usr/local/lib/python3.7/site-packages/jinja2/environment.py:362: DeprecationWarning: The 'with' extension is deprecated and will be removed in Jinja 3.1. This is built in now.  # noqa
    '''
    app.jinja_options = {}

    # 非公開設定ファイル読み込み
    app.config.from_pyfile('settings.py', silent=True)

    # 標準設定ファイル読み込み
    app.config.from_object("config")
    secret_key = app.config['SECRET_KEY'].encode('utf-8')

    init_db(app)
    app.secret_key = secret_key
    login_manager.init_app(app)
    login_manager.login_view = 'user_login'
    return app


app = create_app()
handler = WebhookHandler(app.config['LINE_BOT_CHANNEL_SECRET'])


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


@app.route("/admin/league/<int:league_id>/cancel", methods=("GET", "POST"))
@flask_login.login_required
def admin_league_cancel(league_id: int):
    return AdminLeagueCancelController().render(request, league_id=league_id)


@app.route("/admin/league/notify_recruiting", methods=("GET", "POST"))
@flask_login.login_required
def notify_recruiting():
    if request.method == "POST":
        return PostAdminLeagueNotifyRecruitingController().render(request)


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


@app.errorhandler(Exception)
def handle_exception(e):
    path = "{}/log/error.{}.log".format(os.getcwd(), app.config['ENV'])
    logs = [str(dt.now())]
    if flask_login.current_user.is_authenticated:
        logs.append(flask_login.current_user.id)
    logs.append(traceback.format_exc())
    error_msg = " ".join(logs)
    with open(path, mode='a') as f:
        f.write(error_msg)
    if app.config['ENV'] == "production":
        # ぽのちゃん実験場にエラーログを送る(上限1000文字）
        length = 995 if len(error_msg) > 995 else len(error_msg)
        PonnoNotify(app.config['LINE_NOTIFY_ACCESS_TOKEN_HASH']['development']).execute("...\n" + error_msg[- length:])
    return render_template("error.html", error_message=str(error_msg))


# for flask-login
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


# for flask-login
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


# for line api
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     if (event.source.user_id not in app.config['LINE_BOT_ADMIN_USER_IDS']):
#         return
#     if (event.message.text == 'ここはどこ？'):
#         line_bot_api.reply_message(event.reply_token,
#                                    TextSendMessage(text="{}だよ".format(event.source.group_id)))
