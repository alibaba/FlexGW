# -*- coding: utf-8 -*-
"""
    website.vpn.sts.models
    ~~~~~~~~~~~~~~~~~~~~~~

    vpn sts system models.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from website import db


class Account(db.Model):
    '''dial name.'''
    __tablename__ = 'dial_account'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.String(80))
    created_at = db.Column(db.DateTime)

    def __init__(self, name, password, created_at=datetime.now()):
        self.name = name
        self.password = generate_password_hash(password, method='sha1', salt_length=7)
        self.created_at = created_at

    def __repr__(self):
        return '<Dial Account %s:%s>' % (self.name, self.created_at)

    def get_id(self):
        return unicode(self.id)

    def check_password(self, pw):
        return check_password_hash(self.password, pw)

    def update_password(self, pw):
        self.password = generate_password_hash(pw, method='sha1', salt_length=7)
        db.session.commit()
        return True


class Settings(db.Model):
    """settings for dial or common settings."""
    __tablename__ = 'dial_settings'

    id = db.Column(db.Integer, primary_key=True)
    ipool = db.Column(db.String(80))

    def __init__(self, ipool):
        self.ipool = ipool

    def __repr__(self):
        return '<Settings %s>' % self.id
