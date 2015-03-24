# -*- coding: utf-8 -*-
"""
    website.vpn.sts.forms
    ~~~~~~~~~~~~~~~~~~~~~

    vpn forms:
        /vpn/sts/add
        /vpn/sts/<int:id>/settings
"""


from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField
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
            elif numbers[0] == 100 and numbers[1] >= 64 and numbers[1] <= 127:
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
                                          Length(max=20, message=u'帐号最长为20个字符！'),
                                          Regexp(r'^[\w]+$', message=u"只可包含如下字符：数字、字母、下划线！")])

    start_type = SelectField(u'启动类型',
                             choices=[('add', u'手工连接'), ('start', u'服务启动自动连接')])

    encryption_algorithm = SelectField(u'加密算法',
                                       choices=[('3des', u'3des'), ('cast128', u'cast128'),
                                                ('blowfish128', u'blowfish128'), ('blowfish192', u'blowfish192'),
                                                ('blowfish256', u'blowfish256'), ('aes128', u'aes128'),
                                                ('aes192', u'aes192'), ('aes256', u'aes256'),
                                                ('camellia128', u'camellia128'), ('camellia192', u'camellia192'),
                                                ('camellia256', u'camellia256'), ('null', u'不加密')])

    integrity_algorithm = SelectField(u'签名算法',
                                      choices=[('md5', u'md5'), ('md5_128', u'md5_128'),
                                               ('sha1', u'sha1'), ('sha1_160', u'sha1_160'),
                                               ('aesxcbc', u'aesxcbc'), ('aescmac', u'aescmac'),
                                               ('aes128gmac', u'aes128gmac'), ('aes192gmac', u'aes192gmac'),
                                               ('aes256gmac', u'aes256gmac'), ('sha2_256', u'sha2_256'),
                                               ('sha2_384', u'sha2_384'), ('sha2_512', u'sha2_512'),
                                               ('sha2_256_96', u'sha2_256_96')])

    dh_algorithm = SelectField(u'DH算法',
                               choices=[('modp768', u'modp768(group 1)'), ('modp1024', u'modp1024(group 2)'),
                                        ('modp1536', u'modp1536(group 5)'), ('modp2048', u'modp2048(group 14)'),
                                        ('modp3072', u'modp3072(group 15)'), ('modp4096', u'modp4096(group 16)'),
                                        ('modp6144', u'modp6144(group 17)'), ('modp8192', u'modp8192(group 18)'),
                                        ('modp1024s160', u'modp1024s160(group 22)'), ('modp2048s224', u'modp2048s224(group 23)'),
                                        ('modp2048s256', u'modp2048s256(group 24)'), ('ecp192', u'ecp192(group 25)'),
                                        ('ecp224', u'ecp224(group 26)'), ('ecp256', u'ecp256(group 19)'),
                                        ('ecp384', u'ecp384(group 20)'), ('ecp521', u'ecp521(group 21)'),
                                        ('ecp224bp', u'ecp224bp(group 27)'), ('ecp256bp', u'ecp256bp(group 28)'),
                                        ('ecp384bp', u'ecp384bp(group 29)'), ('ecp512bp', u'ecp512bp(group 30)')])

    local_subnet = TextAreaField(u'本端子网',
                                 validators=[DataRequired(message=u'这是一个必选项！'),
                                             SubNets(message=u"无效的子网")])

    remote_ip = StringField(u'对端公网IP',
                            validators=[DataRequired(message=u'这是一个必选项！'),
                                        PublicIP(message=u'无效的公网地址！')])

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
