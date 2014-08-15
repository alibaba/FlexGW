# -*- coding: utf-8 -*-
"""
    website.docs.views
    ~~~~~~~~~~~~~~~~~~

    vpn views:
        /docs

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from flask import Blueprint, render_template
from flask import url_for, redirect

from flask.ext.login import login_required


docs = Blueprint('docs', __name__, url_prefix='/docs',
                 template_folder='templates')


@docs.route('/')
@login_required
def index():
    return redirect(url_for('docs.issue'))


@docs.route('/issue')
@login_required
def issue():
    return render_template('issue.html')
