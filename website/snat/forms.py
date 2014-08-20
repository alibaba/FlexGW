# -*- coding: utf-8 -*-
"""
    website.snat.forms
    ~~~~~~~~~~~~~~~~~~

    vpn forms:
        /sant

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import Required, IPAddress


class SnatForm(Form):
    source = TextField(u'SNAT源IP（段）',
                       validators=[Required(message=u'这是一个必选项！')])
    gateway = TextField(u'SNAT转发IP',
                        validators=[Required(message=u'这是一个必选项！'),
                                    IPAddress(message=u'无效的ip 地址！')])
