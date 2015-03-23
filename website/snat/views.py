# -*- coding: utf-8 -*-
"""
    website.snat.views
    ~~~~~~~~~~~~~~~~~~

    vpn views:
        /snat
"""


from flask import Blueprint, render_template
from flask import url_for, redirect, flash
from flask import request

from flask.ext.login import login_required

from website.snat.forms import SnatForm
from website.snat.services import iptables_get_snat_rules, iptables_set_snat_rules


snat = Blueprint('snat', __name__, url_prefix='/snat',
                 template_folder='templates',
                 static_folder='static')


@snat.route('/')
@login_required
def index():
    rules = iptables_get_snat_rules()
    if isinstance(rules, list) and not rules:
        flash(u'目前没有任何SNAT配置，如有需要请添加。', 'info')
    return render_template('index.html', rules=rules)


@snat.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = SnatForm()
    if form.validate_on_submit():
        if iptables_set_snat_rules('add', form.source.data, form.gateway.data):
            message = u'添加SNAT 规则成功：%s ==> %s' % (form.source.data, form.gateway.data)
            flash(message, 'success')
            return redirect(url_for('snat.index'))
    return render_template('add.html', form=form)


@snat.route('/del', methods=['POST'])
@login_required
def delete():
    source = request.form['source']
    gateway = request.form['gateway']
    if iptables_set_snat_rules('del', source, gateway):
        message = u'删除SNAT 规则成功：%s ==> %s' % (source, gateway)
        flash(message, 'success')
    return redirect(url_for('snat.index'))
