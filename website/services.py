# -*- coding: utf-8 -*-
"""
    website.services
    ~~~~~~~~~~~~~~~~

    top level services api.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


import subprocess

from threading import Timer


def exec_command(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    # settings exec timeout
    timer = Timer(5, proc.kill, [proc])
    timer.start()
    stdout, stderr = proc.communicate()
    timer.cancel()
    return {'return_code': proc.returncode, 'stdout': stdout,
            'stderr': stderr}
