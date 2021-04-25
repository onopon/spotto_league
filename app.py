#!/home/miyablo/.pyenv/versions/flask_peewee_3.6.4/bin/python
# -*- coding: utf-8 -*-
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
#  from spotto_league.controllers.league_list_controller import LeagueListController
#  from spotto_league.controllers.league_controller import LeagueController
#  from spotto_league.controllers.user.exists_controller import ExistsController as UserExistsController
#  from spotto_league.controllers.user.register_controller import RegisterController as UserRegisterController
#  from spotto_league.controllers.user.post_register_controller import PostRegisterController as PostUserRegisterController
#  from spotto_league.controllers.user.login_controller import LoginController as UserLoginController
#  from spotto_league.controllers.user.post_login_controller import PostLoginController as PostUserLoginController
#  from spotto_league.controllers.user.info_controller import InfoController as UserInfoController
#  from spotto_league.controllers.user.modify_controller import ModifyController as UserModifyController
#  from spotto_league.controllers.user.modify_password_controller import ModifyPasswordController as UserModifyPasswordController
#  from spotto_league.controllers.user.post_modify_controller import PostModifyController as PostUserModifyController
#  from spotto_league.controllers.user.post_modify_password_controller import PostModifyPasswordController as PostUserModifyPasswordController
#  from spotto_league.controllers.user.ranking_controller import RankingController as UserRankingController
#  from spotto_league.controllers.post_league_log_controller import PostLeagueLogController as PostLeagueLogController
#  from spotto_league.controllers.admin.league.register_controller import RegisterController as AdminLeagueRegisterController
#  from spotto_league.controllers.admin.league.modify_controller import ModifyController as AdminLeagueModifyController
#  from spotto_league.controllers.admin.league.post_register_controller import PostRegisterController as PostAdminLeagueRegisterController
#  from spotto_league.controllers.admin.league.league_controller import LeagueController as AdminLeagueController
#  from spotto_league.controllers.admin.league.post_league_controller import PostLeagueController as PostAdminLeagueController
#  from spotto_league.controllers.admin.league.post_league_finish_controller import PostLeagueFinishController as PostAdminLeagueFinishController
#  from spotto_league.controllers.admin.user.register_point_controller import RegisterPointController as AdminUserRegisterPointController
#  from spotto_league.controllers.admin.user.post_register_point_controller import PostRegisterPointController as PostAdminUserRegisterPointController
#  from spotto_league.controllers.admin.user.list_controller import ListController as AdminUserListController
#  from spotto_league.controllers.admin.user.post_list_controller import PostListController as PostAdminUserListController
#  from spotto_league.controllers.user.post_league_join_controller import PostLeagueJoinController as PostUserLeagueJoinController
#  from spotto_league.controllers.user.post_league_cancel_controller import PostLeagueCancelController as PostUserLeagueCancelController
#  from spotto_league.modules.password_util import PasswordUtil
# from spotto_league.models.user import User

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!\n"

@app.route('/hoge')
def hoge():
    return "Hoge World!\n"

# @app.route("/user/register", methods=("GET", "POST"))
# # @auth.login_required
# def user_register():
#     if request.method == "POST":
#         return PostUserRegisterController().render(request)
#     return UserRegisterController().render(request)

if __name__ == '__main__':
    app.run()
