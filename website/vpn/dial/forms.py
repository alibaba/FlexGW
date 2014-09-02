# -*- coding: utf-8 -*-
"""
    website.vpn.dial.forms
    ~~~~~~~~~~~~~~~~~~~~~~

    vpn forms:
        /vpn/dial/add
        /vpn/dial/settings
        /vpn/dial/<int:id>/settings

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length


def _ipool(value):
    try:
        ip = value.split('/')[0]
        mask = int(value.split('/')[1])
    except:
        return False
    if mask < 0 or mask > 32:
        return False
    parts = ip.split('.')
    if len(parts) == 4 and all(x.isdigit() for x in parts):
        numbers = list(int(x) for x in parts)
        if not all(num >= 0 and num < 256 for num in numbers):
            return False
        return True
    return False


def IPool(message=u"无效的地址段"):
    def __ipool(form, field):
        value = field.data
        if not _ipool(value):
            raise ValidationError(message)
    return __ipool


def SubNets(message=u"无效的子网"):
    def __subnets(form, field):
        value = field.data
        parts = [i.strip() for i in value.split(',')]
        if not all(_ipool(part) for part in parts):
            raise ValidationError(message)
    return __subnets


class AddForm(Form):
    name = StringField(u'账号名',
                       validators=[DataRequired(message=u'这是一个必选项！'),
                                   Length(max=20, message=u'帐号最长为20个字符！')])
    password = StringField(u'密码',
                           validators=[DataRequired(message=u'这是一个必选项！')])
    #: submit button
    save = SubmitField(u'保存')
    delete = SubmitField(u'删除')


class SettingsForm(Form):
    ipool = StringField(u'虚拟IP 地址池',
                        validators=[DataRequired(message=u'这是一个必选项！'),
                                    IPool(message=u"无效的IP 地址池")])
    subnet = TextAreaField(u'子网网段',
                           validators=[DataRequired(message=u'这是一个必选项！'),
                                       SubNets(message=u"无效的子网")])


class ConsoleForm(Form):
    '''web console form'''
    #: submit button
    stop = SubmitField(u'关闭')
    start = SubmitField(u'启动')
    re_load = SubmitField(u'下发&重载')
