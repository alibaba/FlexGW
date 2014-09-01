# -*- coding: utf-8 -*-
"""
    website.api.views
    ~~~~~~~~~~~~~~~~~

    vpn views:
        /api/*

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from flask import Blueprint, jsonify

from flask.ext.login import login_required

from website.services import exec_command
from website.vpn.sts.services import VpnServer


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/vpn/<tunnel_name>/traffic/now')
@login_required
def vpn_traffic(tunnel_name):
    vpn = VpnServer()
    return jsonify(vpn.tunnel_traffic(tunnel_name) or [])


@api.route('/vpn/<tunnel_name>/up')
@login_required
def tunnel_up(tunnel_name):
    vpn = VpnServer()
    return jsonify({'result': vpn.tunnel_up(tunnel_name), 'stdout': vpn.c_stdout})


@api.route('/checkupdate')
def check_update():
    cmd = ['/usr/local/flexgw/scripts/update', '--check']
    try:
        r = exec_command(cmd, timeout=10)
    except:
        return jsonify({"message": "run `/usr/local/flexgw/scripts/update --check' Error!"}), 500
    if r['return_code'] != 0:
        return jsonify({"message": "update check Failed!"}), 504
    for line in r['stdout'].split('\n'):
        if ' new ' in line:
            info = u"发现新版本：%s！" % (line.split(':')[1])
            return jsonify({"message": info})
    return jsonify({"message": u"已经是最新版本了！"}), 404
