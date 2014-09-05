# -*- coding: utf-8 -*-
"""
    website.docs.views
    ~~~~~~~~~~~~~~~~~~

    vpn views:
        /docs
"""


from flask import Blueprint, render_template

from flask.ext.login import login_required


docs = Blueprint('docs', __name__, url_prefix='/docs',
                 template_folder='templates',
                 static_folder='static')


@docs.route('/')
@login_required
def index():
    return render_template('docs/guide.html')


@docs.route('/ipsec')
@login_required
def ipsec():
    return render_template('docs/ipsec.html')


@docs.route('/dial')
@login_required
def dial():
    return render_template('docs/dial.html')


@docs.route('/snat')
@login_required
def snat():
    return render_template('docs/snat.html')


@docs.route('/certificate')
@login_required
def certificate():
    return render_template('docs/certificate.html')


@docs.route('/debug')
@login_required
def debug():
    return render_template('docs/debug.html')


@docs.route('/update')
@login_required
def update():
    return render_template('docs/update.html')


@docs.route('/changelog')
@login_required
def changelog():
    return render_template('docs/changelog.html')
