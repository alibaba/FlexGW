# -*- coding: utf-8 -*-
"""
    website.vpn.dial.forms
    ~~~~~~~~~~~~~~~~~~~~~~

    vpn forms:
        /vpn/dial/add
        /vpn/dial/settings
        /vpn/dial/<int:id>/settings
"""


from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Regexp


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
                                   Length(max=20, message=u'帐号最长为20个字符！'),
                                   Regexp(r'^[\w]+$', message=u"只可包含如下字符：数字、字母、下划线！")])
    password = StringField(u'密码',
                           validators=[DataRequired(message=u'这是一个必选项！'),
                                       Length(max=20, message=u'密码最长为20个字符！'),
                                       Regexp(r'^[\w]+$', message=u"只可包含如下字符：数字、字母、下划线！")])
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
    c2c = SelectField(u'允许client 间通信',
                      choices=[('no', u'否'), ('yes', u'是')])
    duplicate = SelectField(u'允许单个账号同时在线',
                            choices=[('no', u'否'), ('yes', u'是')])
    proto = SelectField(u'通信协议',
                        choices=[('udp', u'UDP'), ('tcp', u'TCP')])


class ConsoleForm(Form):
    '''web console form'''
    #: submit button
    stop = SubmitField(u'关闭')
    start = SubmitField(u'启动')
    re_load = SubmitField(u'下发&重载')
