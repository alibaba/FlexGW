# -*- coding: utf-8 -*-
"""
    website.account.services
    ~~~~~~~~~~~~~~~~~~~~~~~~

    account login validate.
"""


from website import login_manager
from website.account.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query_filter_by(id=user_id)
