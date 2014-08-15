# -*- coding: utf-8 -*-
"""
    website.account.views
    ~~~~~~~~~~~~~~~~~~~~~

    account views:
        /login
        /logout
        /settings

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""

from flask import Blueprint, render_template, request
from flask import url_for, session, redirect, json, abort
from flask import current_app

from website.account.models import User
from website.account.forms import LoginForm

from flask.ext.login import login_required, logout_user, login_user
from flask.ext.principal import identity_changed, AnonymousIdentity, Identity


account = Blueprint('account', __name__,
                    template_folder='templates')


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(account=form.account.data).first()
        login_user(user)
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(user.id))
        return redirect(url_for('default'))
    return render_template('login.html', form=form)


@account.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()
    # Remove session
    session.clear()
    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for("account.login"))


@account.route('/account/settings')
@login_required
def settings():
    pass
