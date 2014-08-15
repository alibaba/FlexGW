# -*- coding: utf-8 -*-
"""
    website.vpn.models
    ~~~~~~~~~~~~~~~~~~

    vpn system models.

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from datetime import datetime

from website import db


class Tunnels(db.Model):
    '''tunnels models.'''
    __tablename__ = 'tunnels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True)
    rules = db.Column(db.String(500))
    auth_type = db.Column(db.String(80))
    created_at = db.Column(db.DateTime)

    def __init__(self, name, rules, auth_type, created_at=datetime.now()):
        self.name = name
        self.rules = rules
        self.auth_type = auth_type
        self.created_at = created_at

    def __repr__(self):
        return '<Tunnels %s:%s>' % (self.name, self.created_at)


class Psk(db.Model):
    """psk models."""
    __tablename__ = 'psk'

    id = db.Column(db.Integer, primary_key=True)
    tunnel_id = db.Column(db.Integer, unique=True, index=True)
    data = db.Column(db.String(80))

    def __init__(self, tunnel_id, data):
        self.tunnel_id = tunnel_id
        self.data = data

    def __repr__(self):
        return '<Psk %s>' % self.tunnel_id


class XAuth(db.Model):
    """xauth models."""
    __tablename__ = 'xauth'

    id = db.Column(db.Integer, primary_key=True)
    tunnel_id = db.Column(db.Integer, unique=True, index=True)
    data = db.Column(db.String(80))

    def __init__(self, tunnel_id, data):
        self.tunnel_id = tunnel_id
        self.data = data

    def __repr__(self):
        return '<XAuth %s>' % self.tunnel_id


class Settings(db.Model):
    """settings for dial or common settings."""
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    ipool = db.Column(db.String(80))

    def __init__(self, ipool):
        self.ipool = ipool

    def __repr__(self):
        return '<Settings %s>' % self.id
