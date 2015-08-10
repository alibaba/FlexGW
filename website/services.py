# -*- coding: utf-8 -*-
"""
    website.services
    ~~~~~~~~~~~~~~~~

    top level services api.
"""


import subprocess

from threading import Timer


def exec_command(cmd, timeout=5, stdout=subprocess.PIPE):
    proc = subprocess.Popen(cmd, stdout=stdout,
                            stderr=subprocess.PIPE)
    # settings exec timeout
    timer = Timer(timeout, proc.kill)
    timer.start()
    stdout, stderr = proc.communicate()
    timer.cancel()
    return {'return_code': proc.returncode, 'stdout': stdout,
            'stderr': stderr}
