# -*- coding: utf-8 -*-
"""
    website.snat.services
    ~~~~~~~~~~~~~~~~~~~~~

    snat services api.
"""


import sys

from flask import flash, current_app

from website.services import exec_command


def iptables_get_snat_rules(message=True):
    cmd = ['iptables', '-t', 'nat', '--list-rules']
    try:
        r = exec_command(cmd)
    except:
        current_app.logger.error('[SNAT]: exec_command error: %s:%s', cmd,
                                 sys.exc_info()[1])
        if message:
            flash(u'iptables 程序异常，无法调用，请排查操作系统相关设置！', 'alert')
        return False
    if r['return_code'] != 0:
        current_app.logger.error('[SNAT]: exec_command return: %s:%s:%s', cmd,
                                 r['return_code'], r['stderr'])
        if message:
            message = u"获取规则失败：%s" % r['stderr']
            flash(message, 'alert')
        return False
    rules = []
    for item in r['stdout'].split('\n'):
        if '-j SNAT' in item:
            t = item.split()
            rules.append((t[t.index('-s')+1], t[t.index('--to-source')+1]))
    return rules


def iptables_set_snat_rules(method, source, gateway, message=True):
    methods = {'add': '-A', 'del': '-D'}
    #: check rule exist while add rule
    rules = iptables_get_snat_rules()
    if isinstance(rules, bool) and not rules:
        return False
    if method == 'add' and (source, gateway) in rules:
        if message:
            message = u"该规则已经存在：%s ==> %s" % (source, gateway)
            flash(message, 'alert')
        return False
    #: add rule to iptables
    cmd = 'iptables -t nat %s POSTROUTING -s %s -j SNAT --to-source %s' % (methods[method], source, gateway)
    try:
        r = exec_command(cmd.split())
    except:
        current_app.logger.error('[SNAT]: exec_command error: %s:%s', cmd,
                                 sys.exc_info()[1])
        if message:
            flash(u'iptables 程序异常，无法调用，请排查操作系统相关设置！', 'alert')
        return False
    if r['return_code'] == 0:
        return True
    if message:
        message = u"设置规则失败：%s" % r['stderr']
        flash(message, 'alert')
    current_app.logger.error('[SNAT]: exec_command return: %s:%s:%s', cmd,
                             r['return_code'], r['stderr'])
    return False
