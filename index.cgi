#! /usr/local/bin/python3.7
# -*- coding: utf-8 -*-

import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
from application import app

CGIHandler().run(app)
