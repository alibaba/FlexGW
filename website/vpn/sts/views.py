# -*- coding: utf-8 -*-
"""
    website.vpn.sts.views
    ~~~~~~~~~~~~~~~~~~~~~

    vpn sts views:
        /vpn/sts/add
        /vpn/sts/<int:id>
        /vpn/sts/<int:id>/settings
"""

from flask import Blueprint, render_template
from flask import url_for, redirect
from flask import flash

from website.vpn.sts.forms import AddForm
from website.vpn.sts.forms import ConsoleForm, UpDownForm
from website.vpn.sts.services import vpn_settings, vpn_del
from website.vpn.sts.services import get_tunnels, VpnServer
from website.vpn.sts.models import Tunnels

from flask.ext.login import login_required


sts = Blueprint('sts', __name__, url_prefix='/vpn/sts',
                template_folder='templates')


@sts.route('/')
@login_required
def index():
    form = UpDownForm()
    tunnels = get_tunnels(status=True)
    if not tunnels:
        flash(u'目前没有任何VPN 配置，如有需要请添加。', 'info')
    return render_template('sts/index.html', tunnels=tunnels, form=form)


@sts.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        if not Tunnels.query.filter_by(name=form.tunnel_name.data).first():
            if vpn_settings(form):
                message = u'添加Site-to-Site 隧道成功！'
                flash(message, 'success')
                return redirect(url_for('sts.index'))
        else:
            message = u'该隧道已经存在：%s' % form.tunnel_name.data
            flash(message, 'alert')
    return render_template('sts/add.html', form=form)


@sts.route('/<int:id>/settings', methods=['GET', 'POST'])
@login_required
def settings(id):
    form = AddForm()
    tunnel = get_tunnels(id)
    if form.validate_on_submit():
        if form.delete.data:
            if vpn_del(id):
                message = u'删除隧道%s ：成功！' % tunnel[0]['name']
                flash(message, 'success')
                return redirect(url_for('sts.index'))
        if form.save.data:
            if vpn_settings(form, id):
                flash(u'修改隧道配置成功！', 'success')
                return redirect(url_for('sts.settings', id=id))
    form.local_subnet.data = tunnel[0]['rules']['leftsubnet']
    form.remote_subnet.data = tunnel[0]['rules']['rightsubnet']
    form.start_type.data = tunnel[0]['rules']['auto']
    # Backward compatible v1.1.0
    esp_settings = tunnel[0]['rules']['esp'].split('-')
    form.esp_encryption_algorithm.data = esp_settings[0]
    form.esp_integrity_algorithm.data = esp_settings[1]
    form.esp_dh_algorithm.data = esp_settings[2] if len(esp_settings) == 3 else 'null'
    ike_settings = tunnel[0]['rules'].get('ike', 'aes128-sha1-modp2048').split('-')
    form.ike_encryption_algorithm.data = ike_settings[0]
    form.ike_integrity_algorithm.data = ike_settings[1]
    form.ike_dh_algorithm.data = ike_settings[2]
    return render_template('sts/view.html', tunnel=tunnel[0], form=form)


@sts.route('/<int:id>/flow')
@login_required
def flow(id):
    tunnel = get_tunnels(id, status=True)
    return render_template('sts/flow.html', tunnel=tunnel[0])


@sts.route('/console', methods=['GET', 'POST'])
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
    return render_template('sts/console.html', status=vpn.status, form=form)


@sts.route('/updown', methods=['POST'])
@login_required
def updown():
    form = UpDownForm()
    vpn = VpnServer()
    if form.validate_on_submit():
        if form.up.data and vpn.tunnel_up(form.tunnel_name.data):
            flash(u'隧道连接成功！', 'success')
        if form.down.data and vpn.tunnel_down(form.tunnel_name.data):
            flash(u'隧道断开成功！', 'success')
    return redirect(url_for('sts.index'))
