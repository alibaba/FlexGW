# -*- coding: utf-8 -*-
"""
    website.account.views
    ~~~~~~~~~~~~~~~~~~~~~

    account views:
        /login
        /logout
"""

from flask import Blueprint, render_template
from flask import url_for, session, redirect, request

from website.account.models import User
from website.account.forms import LoginForm

from flask.ext.login import login_required, logout_user, login_user


account = Blueprint('account', __name__,
                    template_folder='templates')


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query_filter_by(username=form.account.data)
        login_user(user)
        return redirect(request.args.get("next") or url_for('default'))
    return render_template('account/login.html', form=form)


@account.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()
    # Remove session
    session.clear()
    return redirect(url_for("account.login"))
