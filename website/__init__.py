# -*- coding: utf-8 -*-
"""
    website
    ~~~~~~~

    ECS VPN Website.
"""

__version__ = '1.1.1'

import os

from flask import Flask
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('websiteconfig.default_settings')
app.config.from_pyfile('application.cfg', silent=True)

import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
website_log = '%s/logs/website.log' % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                   os.path.pardir))
file_handler = TimedRotatingFileHandler(website_log,
                                        'W0', 1, backupCount=7)
file_handler.suffix = '%Y%m%d-%H%M'
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

from flask import request_started, got_request_exception
from website.helpers import log_request, log_exception
request_started.connect(log_request, app)
got_request_exception.connect(log_exception, app)

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from flask_wtf.csrf import CsrfProtect
CsrfProtect(app)

import website.views

from website.account.views import account
from website.vpn.sts.views import sts
from website.vpn.dial.views import dial
from website.snat.views import snat
from website.api.views import api
from website.docs.views import docs
app.register_blueprint(account)
app.register_blueprint(sts)
app.register_blueprint(dial)
app.register_blueprint(snat)
app.register_blueprint(api)
app.register_blueprint(docs)
