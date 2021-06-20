#! /usr/local/bin/python3.7
# -*- coding: utf-8 -*-

import cgitb

# AH02429: Response header name '<!--' contains invalid characters, aborting request, referer: http://0.0.0.0:8080/
# 上記のようなエラーが出た場合、試しにcgitb.enable()の前にContent-Typeを出力してみると、web上でエラーの場所を表示してくれるようになるかも。
# print('Content-Type: text/html')
cgitb.enable()

from wsgiref.handlers import CGIHandler
from application import app

CGIHandler().run(app)
