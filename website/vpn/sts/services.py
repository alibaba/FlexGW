# -*- coding: utf-8 -*-
"""
    website.vpn.sts.services
    ~~~~~~~~~~~~~~~~~~~~~~~~

    vpn site-to-site services api.
"""


import json
import sys
import time

from flask import render_template, flash, current_app

from website import db
from website.services import exec_command
from website.vpn.sts.models import Tunnels


class VpnConfig(object):
    ''' read and set config for vpn config file.'''
    secrets_file = '/etc/strongswan/ipsec.secrets'
    conf_file = '/etc/strongswan/ipsec.conf'

    secrets_template = 'sts/ipsec.secrets'
    conf_template = 'sts/ipsec.conf'

    _auth_types = ['secret']

    def __init__(self, conf_file=None, secrets_file=None):
        if conf_file:
            self.conf_file = conf_file
        if secrets_file:
            self.secrets_file = secrets_file

    def _get_tunnels(self):
        data = Tunnels.query.all()
        if data:
            return [{'id': item.id, 'name': item.name,
                     'psk': item.psk, 'rules': json.loads(item.rules)}
                    for item in data]
        return None

    def _commit_conf_file(self):
        tunnels = self._get_tunnels()
        data = render_template(self.conf_template, tunnels=tunnels)
        try:
            with open(self.conf_file, 'w') as f:
                f.write(data)
        except:
            current_app.logger.error('[Ipsec Services]: commit conf file error: %s:%s',
                                     self.conf_file, sys.exc_info()[1])
            return False
        return True

    def _commit_secrets_file(self):
        data = self._get_tunnels()
        if data:
            tunnels = [{'leftid': i['rules']['leftid'],
                        'rightid': i['rules']['rightid'],
                        'psk': i['psk']} for i in data]
        else:
            tunnels = None
        data = render_template(self.secrets_template, tunnels=tunnels)
        try:
            with open(self.secrets_file, 'w') as f:
                f.write(data)
        except:
            current_app.logger.error('[Ipsec Services]: commit secrets file error: %s:%s',
                                     self.secrets_file, sys.exc_info()[1])
            return False
        return True

    def update_tunnel(self, tunnel_id, tunnel_name, rules, psk):
        #: store to instance
        self.tunnel = Tunnels.query.filter_by(id=tunnel_id).first()
        if self.tunnel is None:
            self.tunnel = Tunnels(tunnel_name, rules, psk)
            db.session.add(self.tunnel)
        else:
            self.tunnel.name = tunnel_name
            self.tunnel.rules = rules
            self.tunnel.psk = psk
        db.session.commit()
        return True

    def delete(self, id):
        tunnel = Tunnels.query.filter_by(id=id).first()
        db.session.delete(tunnel)
        db.session.commit()
        return True

    def commit(self):
        if self._commit_conf_file() and self._commit_secrets_file():
            return True
        return False


class VpnServer(object):
    """vpn server console"""
    def __init__(self):
        self.cmd = None
        self.c_code = None
        self.c_stdout = None
        self.c_stderr = None

    def __repr__(self):
        return '<VpnServer %s:%s:%s:%s>' % (self.cmd, self.c_code,
                                            self.c_stdout, self.c_stderr)

    def _exec(self, cmd, message=None):
        try:
            r = exec_command(cmd)
        except:
            current_app.logger.error('[Ipsec Services]: exec_command error: %s:%s',
                                     cmd, sys.exc_info()[1])
            flash(u'VPN 程序异常，无法调用，请排查操作系统相关设置！', 'alert')
            return False
        #: store cmd info
        self.cmd = cmd
        self.c_code = r['return_code']
        self.c_stdout = [i for i in r['stdout'].split('\n') if i]
        self.c_stderr = [i for i in r['stderr'].split('\n') if i]
        #: check return code
        if r['return_code'] == 0:
            return True
        if message:
            flash(message % r['stderr'], 'alert')
        current_app.logger.error('[Ipsec Services]: exec_command return: %s:%s:%s',
                                 cmd, r['return_code'], r['stderr'])
        return False

    def _tunnel_exec(self, cmd, message=None):
        if not self._exec(cmd, message):
            return False
        #: check return data
        try:
            r = self.c_stdout[-1]
        except IndexError:
            current_app.logger.error('[Ipsec Services]: exec_command return: %s:%s:%s:%s',
                                     cmd, self.c_code, self.c_stdout, self.c_stderr)
            flash(u'命令已执行，但是没有返回数据。', 'alert')
            return False
        #: check return status
        if 'successfully' in r:
            return True
        else:
            current_app.logger.error('[Ipsec Services]: exec_command return: %s:%s:%s:%s',
                                     cmd, self.c_code, self.c_stdout, self.c_stderr)
            message = u'命令已执行，但是没有返回成功状态：%s' % r
            flash(message, 'alert')
            return False

    def _reload_conf(self):
        cmd = ['strongswan', 'reload']
        message = u"VPN 服务配置文件重载失败！%s"
        return self._exec(cmd, message)

    def _rereadsecrets(self):
        cmd = ['strongswan', 'rereadsecrets']
        message = u"VPN 服务密钥文件重载失败！%s"
        return self._exec(cmd, message)

    @property
    def start(self):
        if self.status:
            flash(u'服务已经启动！', 'info')
            return False
        cmd = ['strongswan', 'start']
        message = u"VPN 服务启动失败：%s"
        return self._exec(cmd, message)

    @property
    def stop(self):
        if not self.status:
            flash(u'服务已经停止！', 'info')
            return False
        cmd = ['strongswan', 'stop']
        message = u"VPN 服务停止失败：%s"
        return self._exec(cmd, message)

    @property
    def reload(self):
        tunnel = VpnConfig()
        if not tunnel.commit():
            message = u'VPN 服务配置文件修改失败，请重试。'
            flash(message, 'alert')
            return False
        if not self.status:
            flash(u'设置成功！VPN 服务未启动，请通过「VPN服务管理」启动VPN 服务。', 'alert')
            return False
        if self._reload_conf() and self._rereadsecrets():
            return True
        return False

    @property
    def status(self):
        cmd = ['strongswan', 'status']
        return self._exec(cmd)

    def tunnel_status(self, tunnel_name):
        cmd = ['strongswan', 'status', tunnel_name]
        if self._exec(cmd):
            for item in self.c_stdout:
                if 'INSTALLED' in item:
                    return True
        return False

    def tunnel_up(self, tunnel_name):
        if self.tunnel_status(tunnel_name):
            flash(u'隧道已经连接！', 'info')
            return False
        cmd = ['strongswan', 'up', tunnel_name]
        message = u"隧道启动失败：%s"
        return self._tunnel_exec(cmd, message)

    def tunnel_down(self, tunnel_name):
        if not self.tunnel_status(tunnel_name):
            flash(u'隧道已经断开！', 'info')
            return False
        cmd = ['strongswan', 'down', tunnel_name]
        message = u"隧道停止失败：%s"
        return self._tunnel_exec(cmd, message)

    def tunnel_traffic(self, tunnel_name):
        cmd = ['strongswan', 'statusall', tunnel_name]
        rx_pkts = 0
        tx_pkts = 0
        raw_data = None
        if self._exec(cmd):
            for line in self.c_stdout:
                if 'bytes_i' in line:
                    raw_data = line.replace(',', '').split()
            if not raw_data:
                return False
            if raw_data[raw_data.index('bytes_i')+1].startswith('('):
                #: check Timestamp > 2s, then drop.
                if int(raw_data[raw_data.index('bytes_i')+3].strip('s')) < 2:
                    tx_pkts = raw_data[raw_data.index('bytes_i')+1].strip('(')
            if raw_data[raw_data.index('bytes_o')+1].startswith('('):
                #: check Timestamp > 2s, then drop.
                if int(raw_data[raw_data.index('bytes_o')+3].strip('s')) < 2:
                    rx_pkts = raw_data[raw_data.index('bytes_o')+1].strip('(')
            return {'rx_pkts': int(rx_pkts),
                    'tx_pkts': int(tx_pkts),
                    'time': int(time.time())}
        return False


def vpn_settings(form, tunnel_id=None):
    tunnel = VpnConfig()
    vpn = VpnServer()
    local_subnet = ','.join([i.strip() for i in form.local_subnet.data.split(',')])
    remote_subnet = ','.join([i.strip() for i in form.remote_subnet.data.split(',')])
    rules = {'auto': form.start_type.data, 'esp': 'aes256-sha1-modp1024',
             'left': '0.0.0.0', 'leftsubnet': local_subnet,
             'leftid': form.tunnel_name.data, 'right': form.remote_ip.data,
             'rightsubnet': remote_subnet, 'rightid': form.tunnel_name.data,
             'authby': 'secret'}
    if tunnel.update_tunnel(tunnel_id, form.tunnel_name.data, json.dumps(rules),
                            form.psk.data) and vpn.reload:
        return True
    return False


def vpn_del(id):
    config = VpnConfig()
    vpn = VpnServer()
    tunnel = get_tunnels(id, True)[0]
    if tunnel['status']:
        vpn.tunnel_down(tunnel['name'])
    if config.delete(id) and vpn.reload:
        return True
    return False


def get_tunnels(id=None, status=False):
    if id:
        data = Tunnels.query.filter_by(id=id)
    else:
        data = Tunnels.query.all()
    if data:
        tunnels = [{'id': item.id, 'name': item.name, 'psk': item.psk,
                    'rules': json.loads(item.rules)} for item in data]
        if status:
            vpn = VpnServer()
            for tunnel in tunnels:
                tunnel['status'] = vpn.tunnel_status(tunnel['name'])
        return sorted(tunnels, key=lambda x: x.get('status'), reverse=True)
    return None
