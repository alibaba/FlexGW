# -*- coding: utf-8 -*-
"""
    website.vpn.sts.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~

    vpn site-to-site helpers api.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from website.services import exec_command


def exchange_maskint(mask_int):
    bin_arr = ['0' for i in range(32)]

    for i in xrange(mask_int):
        bin_arr[i] = '1'
    tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return '.'.join(tmpmask)


def exchange_mask(mask):
    count_bit = lambda bin_str: len([i for i in bin_str if i == '1'])
    mask_splited = mask.split('.')
    mask_count = [count_bit(bin(int(i))) for i in mask_splited]
    return sum(mask_count)


def get_localhost_ip():
    cmd = ['/sbin/ifconfig']
    eth_ip = {}
    try:
        r = exec_command(cmd)
    except:
        return False
    if r['return_code'] == 0:
        r_data = r['stdout'].split('\n')
        for index, line in enumerate(r_data):
            if line.startswith('inet addr:'):
                eth_ip[r_data[index-1].split()[0]] = line.split().split(':')[1]
    else:
        return False
    return eth_ip
