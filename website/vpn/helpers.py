# -*- coding: utf-8 -*-
"""
    website.vpn.helpers
    ~~~~~~~~~~~~~~~~~~~

    vpn helpers api.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


def ipsec_conf_parser(file):
    with open(file, mode='r') as f:
        raw_data = [l.strip() for l in f.readlines() if l.strip()]
    tunnels = {}
    tunnel = None
    for line in raw_data:
        #: continue while read comment string.
        if line.startswith('#'):
            continue
        #: continue while read config string.
        if line.startswith('config'):
            continue
        #: process conn name
        if line.startswith('conn'):
            if line.split()[1].startswith('%'):
                continue
            else:
                tunnel = line.split()[1]
                tunnels[tunnel] = {}
                continue
        #: process config key=value
        if tunnel:
            data = line.strip().split('=')
            tunnels[tunnel][data[0].strip()] = data[1].strip()
    return tunnels
