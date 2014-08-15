# -*- coding: utf-8 -*-
"""
    website.views
    ~~~~~~~~~~~~~

    top level views.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""

from flask import request, make_response, render_template
from flask import g, abort, jsonify, flash, redirect, url_for

from flask.ext.login import login_required, current_user

from website import app


@app.before_request
def before_request():
    g.user_id = None
    g.user_account = None
    if not current_user.is_anonymous():
        g.user_id = current_user.get_id()
        g.user_account = current_user.account


@app.route('/')
@login_required
def default():
    if not current_user.member_permission.can():
        flash(u' :)')
        return redirect(url_for('account.login'))
    return redirect(url_for('vpn.index'))


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')
