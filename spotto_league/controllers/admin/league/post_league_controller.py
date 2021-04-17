import asyncio
import json
from typing import Dict, Any, List
from collections import defaultdict
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template, redirect, url_for
from flask_login import current_user
from spotto_league.models.league import League
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail
from spotto_league.database import db


class PostLeagueController(BaseController):
    __slots__ = ['_league']
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        self._league = League.find_by_id(kwargs["league_id"])
        if not self._league:
            raise Exception("League: {} does not exist". kwargs["league_id"])
        league_member_ids = request.form.getlist('enabled_league_member_ids')
        # TODO: リーグ戦最低人数を決める
        if len(league_member_ids) < 2:
            raise Exception("League member less than 2")

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        session = db.session
        self._league.session.close()
        league_member_ids = [int(m_id) for m_id in request.form.getlist('enabled_league_member_ids')]
        for member in self._league.members:
#            member.session.close()
            if member.id in league_member_ids:
                member.enabled = True
            else:
                member.enabled = False
            member.save()
#            session.add(member)
        self._league.ready()
        self._league.save()
#        session.add(self._league)
#        session.commit()
        return redirect(url_for('league_list', login_name=current_user.login_name))
