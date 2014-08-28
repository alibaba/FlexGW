#!/usr/local/ecs-vpn/pyenv/versions/2.7.6/bin/python
# -*- coding: utf-8 -*-
"""
    initdb
    ~~~~~~

    initdb for website.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""

import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from website import db


def init_db():
    '''db.drop_all() && db.create_all()'''
    db.drop_all()
    print 'Drop table ok.'
    db.create_all()
    print 'Create table ok.'
    print 'Done!'


if __name__ == '__main__':
    init_db()
