# -*- coding: utf-8 -*-
"""
    website.account.services
    ~~~~~~~~~~~~~~~~~~~~~~~~

    account login validate.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""

from flask import redirect, current_app
from flask.ext.login import current_user, login_user
from flask.ext.principal import identity_loaded, RoleNeed, UserNeed
from flask.ext.principal import Identity, identity_changed

from website import app, login_manager, db
from website.account.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'account'):
        identity.provides.add(UserNeed(current_user.account))
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role))
