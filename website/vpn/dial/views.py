# -*- coding: utf-8 -*-
"""
    website.vpn.dial.views
    ~~~~~~~~~~~~~~~~~~~~~~

    vpn sts views:
        /vpn/dial/settings
        /vpn/dial/add
        /vpn/dial/<int:id>
        /vpn/dial/<int:id>/settings
"""

from flask import Blueprint, render_template
from flask import url_for, redirect
from flask import flash

from flask.ext.login import login_required

from website.vpn.dial.services import get_accounts, account_update, account_del
from website.vpn.dial.services import VpnServer, settings_update
from website.vpn.dial.forms import AddForm, SettingsForm, ConsoleForm
from website.vpn.dial.models import Account, Settings


dial = Blueprint('dial', __name__, url_prefix='/vpn/dial',
                 template_folder='templates',
                 static_folder='static')


@dial.route('/')
@login_required
def index():
    accounts = get_accounts(status=True)
    if not accounts:
        flash(u'目前没有任何VPN 配置，如有需要请添加。', 'info')
    return render_template('dial/index.html', accounts=accounts)


@dial.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    settings = Settings.query.get(1)
    if not settings:
        flash(u'提示：请先进行「设置」再添加VPN 账号。', 'alert')
        return redirect(url_for('dial.settings'))
    form = AddForm()
    if form.validate_on_submit():
        if not Account.query.filter_by(name=form.name.data).first():
            if account_update(form):
                message = u'添加VPN 拨号账号成功！'
                flash(message, 'success')
                return redirect(url_for('dial.index'))
        else:
            message = u'该账号已经存在：%s' % form.name.data
            flash(message, 'alert')
    return render_template('dial/add.html', form=form)


@dial.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    settings = Settings.query.get(1)
    if form.validate_on_submit():
        if settings_update(form):
            flash(u'修改配置成功！注：修改「虚拟IP 地址池」之后，需手工调整相应的SNAT 设置！', 'success')
            return redirect(url_for('dial.settings'))
    if settings:
        form.subnet.data = settings.subnet
        form.c2c.data = settings.c2c
        form.duplicate.data = settings.duplicate
    return render_template('dial/settings.html', settings=settings, form=form)


@dial.route('/<int:id>/settings', methods=['GET', 'POST'])
@login_required
def id_settings(id):
    form = AddForm()
    account = get_accounts(id)
    if form.validate_on_submit():
        if form.delete.data:
            if account_del(id):
                message = u'删除账号%s ：成功！' % account[0]['name']
                flash(message, 'success')
                return redirect(url_for('dial.index'))
        if form.save.data:
            if account_update(form, id):
                flash(u'修改账号配置成功！', 'success')
                return redirect(url_for('dial.id_settings', id=id))
    return render_template('dial/view.html', account=account[0], form=form)


@dial.route('/console', methods=['GET', 'POST'])
@login_required
def console():
    form = ConsoleForm()
    vpn = VpnServer()
    if form.validate_on_submit():
        if form.stop.data and vpn.stop:
            flash(u'VPN 服务停止成功！', 'success')
        if form.start.data and vpn.start:
            flash(u'VPN 服务启动成功！', 'success')
        if form.re_load.data and vpn.reload:
            flash(u'VPN 服务配置生效完成！', 'success')
        return redirect(url_for('dial.console'))
    return render_template('dial/console.html', status=vpn.status, form=form)


@dial.route('/download')
@login_required
def download():
    return render_template('dial/download.html')
