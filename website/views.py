# -*- coding: utf-8 -*-
"""
    website.views
    ~~~~~~~~~~~~~

    top level views.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from flask import g, redirect, url_for

from flask.ext.login import login_required, current_user

from website import app


@app.before_request
def before_request():
    g.account = None
    if not current_user.is_anonymous():
        g.account = current_user.username


@app.route('/')
@login_required
def default():
    return redirect(url_for('sts.index'))
