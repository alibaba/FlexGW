# -*- coding: utf-8 -*-
"""
    website.snat.forms
    ~~~~~~~~~~~~~~~~~~

    vpn forms:
        /sant
"""


from flask_wtf import Form
from wtforms import TextField, ValidationError
from wtforms.validators import Required, IPAddress


def IPorNet(message=u"无效的IP 或网段！"):
    def _ipornet(form, field):
        value = field.data
        ip = value.split('/')[0]
        if '/' in value:
            try:
                mask = int(value.split('/')[1])
            except:
                raise ValidationError(message)
            if mask < 0 or mask > 32:
                    raise ValidationError(message)
        parts = ip.split('.')
        if len(parts) == 4 and all(x.isdigit() for x in parts):
            numbers = list(int(x) for x in parts)
            if not all(num >= 0 and num < 256 for num in numbers):
                raise ValidationError(message)
            return True
        raise ValidationError(message)
    return _ipornet


class SnatForm(Form):
    source = TextField(u'需转换的源IP（或网段）',
                       validators=[Required(message=u'这是一个必选项！'),
                                   IPorNet(message=u"无效的IP 或网段！")])
    gateway = TextField(u'转换后的IP',
                        validators=[Required(message=u'这是一个必选项！'),
                                    IPAddress(message=u'无效的IP 地址！')])
