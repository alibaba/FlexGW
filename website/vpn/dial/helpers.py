# -*- coding: utf-8 -*-
"""
    website.vpn.dial.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~

    vpn dial helpers api.
"""


import sys

from flask import current_app

from website.services import exec_command


def exchange_maskint(mask_int):
    bin_arr = ['0' for i in range(32)]

    for i in xrange(mask_int):
        bin_arr[i] = '1'
    tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return '.'.join(tmpmask)


def get_localhost_ip():
    cmd = ['/sbin/ifconfig']
    eth_ip = {}
    try:
        r = exec_command(cmd)
    except:
        current_app.logger.error('[Dial Helpers]: exec_command error: %s:%s', cmd,
                                 sys.exc_info()[1])
        return False
    if r['return_code'] == 0:
        r_data = r['stdout'].split('\n')
        for index, line in enumerate(r_data):
            if line.startswith('inet addr:'):
                eth_ip[r_data[index-1].split()[0]] = line.split().split(':')[1]
    else:
        current_app.logger.error('[Dial Helpers]: exec_command return: %s:%s:%s', cmd,
                                 r['return_code'], r['stderr'])
        return False
    return eth_ip
