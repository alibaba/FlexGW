# -*- coding: utf-8 -*-
"""
    website.account
    ~~~~~~~~~~~~~~~

    website account blueprint.
"""

from website import login_manager
from website.account.services import load_user


login_manager.login_view = "account.login"
login_manager.login_message = None
