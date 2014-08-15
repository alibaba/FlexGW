# -*- coding: utf-8 -*-
"""
    website.vpn.views
    ~~~~~~~~~~~~~~~~~~~~~

    vpn views:
        /vpn/add
        /vpn/<int:id>
        /vpn/<int:id>/settings

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""

from flask import Blueprint, render_template
from flask import url_for, redirect
from flask import flash

from website.vpn.forms import StsAddForm, DialAddForm, DialSettings
from website.vpn.forms import ConsoleForm, UpDownForm
from website.vpn.services import sts_vpn_settings, dial_vpn_settings, vpn_del
from website.vpn.services import get_tunnels, get_tunnel_psk, get_tunnel_xauth
from website.vpn.services import VpnServer
from website.vpn.models import Tunnels, Settings

from flask.ext.login import login_required


vpn = Blueprint('vpn', __name__, url_prefix='/vpn',
                template_folder='templates')


@vpn.route('/')
@login_required
def index():
    return redirect(url_for('vpn.sts_index'))


@vpn.route('/sts')
@login_required
def sts_index():
    form = UpDownForm()
    tunnels = get_tunnels(status=True)
    if not tunnels:
        flash(u'目前没有任何VPN 配置，如有需要请添加。', 'info')
    return render_template('sts/index.html', tunnels=tunnels, form=form)


@vpn.route('/sts/add', methods=['GET', 'POST'])
@login_required
def sts_add():
    form = StsAddForm()
    if form.validate_on_submit():
        if not Tunnels.query.filter_by(name=form.tunnel_name.data).first():
            if sts_vpn_settings(form):
                message = u'添加Site-to-Site 隧道成功！'
                flash(message, 'success')
                return redirect(url_for('vpn.index'))
        else:
            message = u'该隧道已经存在：%s' % form.tunnel_name.data
            flash(message, 'alert')
    return render_template('sts/add.html', form=form)


@vpn.route('/sts/<int:id>/settings', methods=['GET', 'POST'])
@login_required
def sts_settings(id):
    form = StsAddForm()
    tunnel = get_tunnels(id)
    tunnel[0]['psk'] = get_tunnel_psk(id)
    if form.validate_on_submit():
        if form.delete.data:
            if vpn_del(id):
                message = u'删除隧道%s ：成功！' % tunnel[0]['name']
                flash(message, 'success')
                return redirect(url_for('vpn.sts_index'))
        if form.save.data:
            if sts_vpn_settings(form, id):
                flash(u'修改隧道配置成功！', 'success')
                return redirect(url_for('vpn.sts_settings', id=id))
    form.remote_subnet.data = tunnel[0]['rules']['rightsubnet']
    form.start_type.data = tunnel[0]['rules']['auto']
    form.protocol_type.data = tunnel[0]['rules']['esp']
    return render_template('sts/view.html', tunnel=tunnel[0], form=form)


@vpn.route('/sts/<int:id>/flow')
@login_required
def sts_flow(id):
    tunnel = get_tunnels(id, status=True)
    return render_template('flow.html', tunnel=tunnel[0])


@vpn.route('/dial')
@login_required
def dial_index():
    form = UpDownForm()
    tunnels = get_tunnels(status=True, type='xauth')
    if not tunnels:
        flash(u'目前没有任何VPN 配置，如有需要请添加。', 'info')
    return render_template('dial/index.html', tunnels=tunnels, form=form)


@vpn.route('/dial/add', methods=['GET', 'POST'])
@login_required
def dial_add():
    form = DialAddForm()
    if form.validate_on_submit():
        if not Tunnels.query.filter_by(name=form.account.data).first():
            if dial_vpn_settings(form):
                message = u'添加VPN 拨号账号成功！'
                flash(message, 'success')
                return redirect(url_for('vpn.dial_index'))
        else:
            message = u'该隧道已经存在：%s' % form.account.data
            flash(message, 'alert')
    return render_template('dial/add.html', form=form)


@vpn.route('/dial/settings', methods=['GET', 'POST'])
@login_required
def dial_settings():
    form = DialSettings()
    if form.validate_on_submit():
        pass
    return render_template('dial/settings.html', form=form)


@vpn.route('/dial/<int:id>/settings', methods=['GET', 'POST'])
@login_required
def dial_id_settings(id):
    form = DialAddForm()
    tunnel = get_tunnels(id, type='xauth')
    tunnel[0]['psk'] = get_tunnel_psk(id)
    tunnel[0]['xauth'] = get_tunnel_xauth(id)
    if form.validate_on_submit():
        if form.delete.data:
            if vpn_del(id, type='xauth'):
                message = u'删除隧道%s ：成功！' % tunnel[0]['name']
                flash(message, 'success')
                return redirect(url_for('vpn.dial_index'))
        if form.save.data:
            if dial_vpn_settings(form, id):
                flash(u'修改隧道配置成功！', 'success')
                return redirect(url_for('vpn.dial_settings', id=id))
    return render_template('dial/view.html', tunnel=tunnel[0], form=form)


@vpn.route('/dial/<int:id>/flow')
@login_required
def dial_flow(id):
    tunnel = get_tunnels(id, status=True, type='xauth')
    return render_template('dial/flow.html', tunnel=tunnel)


@vpn.route('/console', methods=['GET', 'POST'])
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
    return render_template('console.html', form=form)


@vpn.route('updown', methods=['POST'])
@login_required
def updown():
    form = UpDownForm()
    vpn = VpnServer()
    if form.validate_on_submit():
        if form.up.data and vpn.tunnel_up(form.tunnel_name.data):
            flash(u'隧道连接成功！', 'success')
        if form.down.data and vpn.tunnel_down(form.tunnel_name.data):
            flash(u'隧道断开成功！', 'success')
    return redirect(url_for('vpn.sts_index'))
