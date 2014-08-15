# -*- coding: utf-8 -*-
"""
    website.api.views
    ~~~~~~~~~~~~~~~~~

    vpn views:
        /api/*

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from flask import Blueprint, render_template
from flask import url_for, redirect, flash
from flask import request, jsonify

from flask.ext.login import login_required

from website.vpn.services import VpnServer


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/vpn/<tunnel_name>/traffic/now')
@login_required
def vpn_traffic(tunnel_name):
    vpn = VpnServer()
    return jsonify(vpn.tunnel_traffic(tunnel_name))


@api.route('/vpn/<tunnel_name>/up')
@login_required
def tunnel_up(tunnel_name):
    vpn = VpnServer()
    return jsonify({'result': vpn.tunnel_up(tunnel_name), 'stdout': vpn.c_stdout})
