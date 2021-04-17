import asyncio
import datetime
from spotto_league.controllers.base_controller import BaseController
from werkzeug.wrappers import BaseRequest, BaseResponse
from flask import Flask, request, render_template, redirect, url_for
from spotto_league.models.place import Place
from spotto_league.models.league import League

MODE_FIND_PLACE = 0
MODE_MAKE_PLACE = 1


class PostRegisterController(BaseController):
    __slots__ = ["_place"]
    # override
    @asyncio.coroutine
    def validate(self, request: BaseRequest, **kwargs) -> None:
        date_str = request.form.get("date")
        start_at_str = request.form.get("start_at")
        end_at_str = request.form.get("end_at")
        name = request.form.get("name")
        game_count = request.form.get("game_count")
        join_end_at_str = request.form.get("join_end_at")
        targets = [date_str, start_at_str, end_at_str, name, game_count, join_end_at_str]
        if any([len(target) == 0 for target in targets]):
            raise Exception("必要なデータが入力されていません。")

        place_mode = int(request.form.get("placetab"))
        if place_mode == MODE_FIND_PLACE:
            place_id = int(request.form.get("place-select"))
            self._place = Place.find_by_id(place_id)
            if not self._place:
                raise Exception("Place: {} は存在しません。".format(place_id))
        elif place_mode == MODE_MAKE_PLACE:
            place_name = request.form.get("place-name")
            url = request.form.get("url")
            capacity = request.form.get("capacity")
            if any([len(target) == 0 for target in [place_name, url, capacity]]):
                raise Exception("会場に関する必要なデータが入力されていません。")
            self._place = Place()
            self._place.name = place_name
            self._place.url = url
            self._place.capacity = int(capacity)
        else:
            raise Exeption()

    # override
    @asyncio.coroutine
    def get_layout(self, request: BaseRequest, **kwargs) -> BaseResponse:
        date_str = request.form.get("date")
        start_at = request.form.get("start_at")
        end_at = request.form.get("end_at")
        name = request.form.get("name")
        game_count = request.form.get("game_count")
        join_end_at = request.form.get("join_end_at")

        league = League()
        league.date = date_str
        league.start_at = start_at
        league.end_at = end_at
        league.name = name
        league.game_count = int(game_count)
        league.join_end_at = join_end_at

        self._place.save()
        league.place_id = self._place.id
        league.save()
        return redirect(url_for('league_list'))
