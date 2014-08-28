#!/usr/local/ecs-vpn/pyenv/versions/2.7.6/bin/python
# -*- coding: utf-8 -*-
"""
    openvpn-auth
    ~~~~~~~~~~~~

    openvpn account auth scripts.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


import os
import sys

import sqlite3


DATABASE = '%s/instance/website.db' % os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))


def __query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.row_factory = sqlite3.Row
    cur = cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def _auth(name, password):
    account = __query_db('select * from dial_account where name = ?', [name], one=True)
    if account is None:
        sys.exit(1)
    elif account['password'] == password:
        sys.exit(0)
    sys.exit(1)


if __name__ == '__main__':
    _auth(os.environ['username'], os.environ['password'])
