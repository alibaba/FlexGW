# -*- coding: utf-8 -*-
"""
    website.account.models
    ~~~~~~~~~~~~~~~~~~~~~~

    account system models.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


import string

from datetime import datetime

from werkzeug import cached_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.principal import Permission, RoleNeed, UserNeed

from website import db


class User(db.Model):
    _member = 1
    _master = 0

    _pass_seed = string.ascii_letters + string.digits + '!@#$%^&*()'

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.String(80))
    role = db.Column(db.Integer, default=0)
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)

    def __init__(self, account, password, created_at=datetime.now()):
        self.account = account
        self.password = generate_password_hash(password, method='sha1', salt_length=7)
        self.created_at = created_at

    def __repr__(self):
        return '<User {0}:{1}:{2}>'.format(self.account, self.role, self.created_at)

    def is_active(self):
        return self.enabled

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def owner_permission(self):
        return Permission(UserNeed(self.account))

    def get_id(self):
        return unicode(self.id)

    def check_password(self, pw):
        return check_password_hash(self.password, pw)

    def update_password(self, pw):
        self.password = generate_password_hash(pw, method='sha1', salt_length=7)
        db.session.commit()
        return True

    @cached_property
    def master_permission(self):
        return Permission(RoleNeed('master'))

    @cached_property
    def member_permission(self):
        return Permission(RoleNeed('member'))

    @property
    def is_member(self):
        return self.role == self._member

    @property
    def is_master(self):
        return self.role == self._master

    @property
    def roles(self):
        if self.is_master:
            return ['member', 'master']
        elif self.is_member:
            return ['member']
