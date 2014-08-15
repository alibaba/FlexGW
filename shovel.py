# -*- coding: utf-8 -*-
"""
    shovel
    ~~~~~~

    some utility tasks for website.

    Usage::

        pip install shovel
        shovel help

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""

import sys
import subprocess
import os

from shovel import task

sys.path.append(os.getcwd())
from website import db
from website.account.models import User


def exec_command(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return {'return_code': proc.wait(), 'stdout': proc.stdout.read()}


@task
def init_db():
    '''db.drop_all() && db.create_all()'''
    db.drop_all()
    print 'Drop table ok.'
    db.create_all()
    print 'Create table ok.'
    print 'Done!'


@task
def add_account(account, password):
    '''add account for user.'''
    user = User(account, password)
    db.session.add(user)
    db.session.commit()
    print 'Done!'


@task
def enable_account(account, role):
    '''setting user role.'''
    roles = {'applicant': 10, 'member': 1, 'master': 0}
    user = User.query.filter_by(account=account).first()
    user.role = roles[role]
    db.session.commit()
    print 'ok: {0} -> {1}({2})'.format(account, role, roles[role])


@task
def restart_website():
    '''restart gunicorn'''
    pass
