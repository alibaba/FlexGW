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


def IPool(message=u"无效的地址段"):
    def _ipool(form, field):
        value = field.data
        try:
            ip = value.split('/')[0]
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
    return _ipool


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
                           validators=[DataRequired(message=u'这是一个必选项！')])


class ConsoleForm(Form):
    '''web console form'''
    #: submit button
    stop = SubmitField(u'关闭')
    start = SubmitField(u'启动')
    re_load = SubmitField(u'下发&重载')
