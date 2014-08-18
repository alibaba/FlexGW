# -*- coding: utf-8 -*-
"""
    website.vpn.sts.services
    ~~~~~~~~~~~~~~~~~~~~~~~~

    vpn site-to-site services api.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from flask import render_template, flash

from website import db
from website.services import exec_command
from website.vpn.dial.models import Account, Settings
from website.vpn.dial.helpers import exchange_maskint


class VpnConfig(object):
    ''' read and set config for vpn config file.'''
    conf_file = '/etc/openvpn/server.conf'

    conf_template = 'dial/server.conf'

    def __init__(self, conf_file=None):
        if conf_file:
            self.conf_file = conf_file

    def _get_settings(self):
        data = Settings.query.get(1)
        if data:
            return data.ipool, data.subnet
        return None

    def _commit_conf_file(self):
        r_ipool, r_subnet = self._get_settings()
        ipool = "%s %s" % (r_ipool.split('/')[0].strip(),
                           exchange_maskint(int(r_ipool.split('/')[1].strip())))
        subnet = "%s %s" % (r_subnet.split('/')[0].strip(),
                            exchange_maskint(int(r_subnet.split('/')[1].strip())))
        data = render_template(self.conf_template, ipool=ipool, subnet=subnet)
        try:
            with open(self.conf_file, 'w') as f:
                f.write(data)
        except:
            return False
        return True

    def update_account(self, id, name, password):
        account = Account.query.filter_by(id=id).first()
        if account is None:
            account = Account(name, password)
            db.session.add(account)
        else:
            account.name = name
            account.password = password
        db.session.commit()
        return True

    def update_settings(self, ipool, subnet):
        settings = Settings.query.get(1)
        if settings is None:
            settings = Settings(ipool, subnet)
            db.session.add(settings)
        else:
            settings.ipool = ipool
            settings.subnet = subnet
        db.session.commit()
        return True

    def delete(self, id):
        account = Account.query.filter_by(id=id).first()
        db.session.delete(account)
        db.session.commit()
        return True

    def commit(self):
        if self._commit_conf_file():
            return True
        return False


class VpnServer(object):
    """vpn server console"""
    log_file = '/etc/openvpn/openvpn-status.log'

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
            flash(u'VpnServer 程序异常，无法调用，请排查操作系统相关设置！', 'alert')
            return False
        #: store cmd info
        self.cmd = cmd
        self.c_code = r['return_code']
        self.c_stdout = r['stdout']
        self.c_stderr = r['stderr']
        #: check return code
        if r['return_code'] == 0:
            return True
        if message:
            flash(message % r['stderr'], 'alert')
        return False

    def _reload_conf(self):
        cmd = ['service', 'openvpn', 'reload']
        message = u"VPN 服务配置文件加载失败：%s"
        return self._exec(cmd, message)

    @property
    def start(self):
        cmd = ['service', 'openvpn', 'start']
        message = u"VPN 服务启动失败：%s"
        return self._exec(cmd, message)

    @property
    def stop(self):
        cmd = ['service', 'openvpn', 'stop']
        message = u"VPN 服务停止失败：%s"
        return self._exec(cmd, message)

    @property
    def reload(self):
        tunnel = VpnConfig()
        if not tunnel.commit():
            message = u'VPN 服务配置文件下发失败。'
            flash(message, 'alert')
            return False
        if self._reload_conf():
            return True
        return False

    @property
    def status(self):
        cmd = ['service', 'openvpn', 'status']
        return self._exec(cmd)

    def account_status(self, account_name):
        try:
            with open(self.log_file) as f:
                raw_data = f.readlines()
        except:
            return False
        for line in raw_data:
            if line.startswith('CLIENT_LIST,%s,' % account_name):
                data = line.split(',')
                return {'rip': '%s' % data[2], 'vip': '%s' % data[3],
                        'br': data[4], 'bs': data[5], 'ct': data[7]}
        return False

    def tunnel_traffic(self, tunnel_name):
        pass


def get_accounts(id=None, status=False):
    if id:
        data = Account.query.filter_by(id=id)
    else:
        data = Account.query.all()

    if data:
        accounts = [{'id': i.id, 'name': i.name,
                     'password': i.password, 'created_at': i.created_at}
                    for i in data]
        if status:
            vpn = VpnServer()
            for account in accounts:
                status = vpn.account_status(account['name'])
                if status:
                    account['rip'] = status['rip']
                    account['vip'] = status['vip']
                    account['br'] = status['br']
                    account['bs'] = status['bs']
                    account['ct'] = status['ct']
        return accounts
    return None

def account_update(form, id=None):
    account = VpnConfig()
    vpn = VpnServer()
    if account.update_account(id, form.name.data, form.password.data) and vpn.reload:
        return True
    return False

def account_del(id):
    config = VpnConfig()
    vpn = VpnServer()
    if config.delete(id) and vpn.reload:
        return True
    return False

def settings_update(form):
    account = VpnConfig()
    vpn = VpnServer()
    if account.update_settings(form.ipool.data, form.subnet.data) and vpn.reload:
        return True
    return False
