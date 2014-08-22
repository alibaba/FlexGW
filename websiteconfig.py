# -*- coding: utf-8 -*-
"""
    websiteconfig
    ~~~~~~~~~~~~~

    default config for website.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""

import os


class default_settings(object):
    DEBUG = True
    TESTING = True

    SECRET_KEY = '\x7f\x89q\x87v~\x87~\x86U\xb1\xa8\xb5=v\xaf\xb0\xdcn\xfa\xea\xeb?\x99'

    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/instance/website.db' % os.path.abspath(os.path.dirname(__file__))
