#!/usr/local/flexgw/python/bin/python
# -*- coding: utf-8 -*-
"""
    website db migrate manager
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    for manage db migrate.
"""


import sys
import os

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from website import app, db


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
