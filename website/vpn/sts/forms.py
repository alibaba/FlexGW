# -*- coding: utf-8 -*-
"""
    website.vpn.sts.forms
    ~~~~~~~~~~~~~~~~~~~~~

    vpn forms:
        /vpn/sts/add
        /vpn/sts/<int:id>/settings

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms import ValidationError
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


def SubNets(message=u"无效的子网"):
    def __subnets(form, field):
        value = field.data
        parts = [i.strip() for i in value.split(',')]
        if not all(_ipool(part) for part in parts):
            raise ValidationError(message)
    return __subnets


def PublicIP(message=u"无效的公网地址！"):
    def _publicip(form, field):
        value = field.data
        parts = value.split('.')
        if len(parts) == 4 and all(x.isdigit() for x in parts):
            numbers = list(int(x) for x in parts)
            if numbers[0] == 10:
                raise ValidationError(message)
            elif numbers[0] == 192 and numbers[1] == 168:
                raise ValidationError(message)
            elif numbers[0] == 172 and numbers[1] >= 16 and numbers[1] <= 31:
                raise ValidationError(message)
            elif not all(num >= 0 and num < 256 for num in numbers):
                raise ValidationError(message)
            return True
        raise ValidationError(message)
    return _publicip


class AddForm(Form):
    tunnel_name = StringField(u'隧道ID',
                              validators=[DataRequired(message=u'这是一个必选项！'),
                                          Length(max=20, message=u'帐号最长为20个字符！')])
    start_type = SelectField(u'启动类型',
                             choices=[('add', u'手工连接'), ('start', u'服务启动自动连接')])
    local_subnet = TextAreaField(u'本端子网',
                                  validators=[DataRequired(message=u'这是一个必选项！'),
                                              SubNets(message=u"无效的子网")])
    remote_ip = StringField(u'对端EIP',
                            validators=[DataRequired(message=u'这是一个必选项！'),
                                        PublicIP(message=u'EIP 应该为真实有效的公网IP 地址！')])
    remote_subnet = TextAreaField(u'对端子网',
                                  validators=[DataRequired(message=u'这是一个必选项！'),
                                              SubNets(message=u"无效的子网")])
    psk = StringField(u'预共享秘钥',
                      validators=[DataRequired(message=u'这是一个必选项！')])
    #: submit button
    save = SubmitField(u'保存')
    delete = SubmitField(u'删除')


class ConsoleForm(Form):
    '''web console form'''
    #: submit button
    stop = SubmitField(u'关闭')
    start = SubmitField(u'启动')
    re_load = SubmitField(u'下发&重载')


class UpDownForm(Form):
    """for tunnel up and down."""
    tunnel_name = StringField(u'隧道名称')
    #: submit button
    up = SubmitField(u'连接')
    down = SubmitField(u'断开')
