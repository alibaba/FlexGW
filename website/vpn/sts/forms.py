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

    ike_encryption_algorithm = SelectField(u'IKEv2 加密算法',
                                           choices=[('3des', u'3DES'), ('aes128', u'AES128'),
                                                    ('aes192', u'AES192'), ('aes256', u'AES256')])

    ike_integrity_algorithm = SelectField(u'IKEv2 验证算法',
                                          choices=[('md5', u'MD5'), ('sha1', u'SHA1'),
                                                   ('sha2_256', u'SHA2-256'), ('sha2_384', u'SHA2-384'),
                                                   ('sha2_512', u'SHA2-512'), ('aesxcbc', u'AES-XCBC'),
                                                   ('aescmac', u'AES-CMAC')])

    ike_dh_algorithm = SelectField(u'IKEv2 DH 组',
                                   choices=[('modp768', u'Group 1 modp768'), ('modp1024', u'Group 2 modp1024'),
                                            ('modp1536', u'Group 5 modp1536'), ('modp2048', u'Group 14 modp2048'),
                                            ('modp3072', u'Group 15 modp3072'), ('modp4096', u'Group 16 modp4096'),
                                            ('modp6144', u'Group 17 modp6144'), ('modp8192', u'Group 18 modp8192'),
                                            ('ecp256', u'Group 19 ecp256'), ('ecp384', u'Group 20 ecp384'),
                                            ('ecp521', u'Group 21 ecp521'), ('modp1024s160', u'Group 22 modp1024s160'),
                                            ('modp2048s224', u'Group 23 modp2048s224'), ('modp2048s256', u'Group 24 modp2048s256'),
                                            ('ecp192', u'Group 25 ecp192'), ('ecp224', u'Group 26 ecp224'),
                                            ('ecp224bp', u'Group 27 ecp224bp'), ('ecp256bp', u'Group 28 ecp256bp'),
                                            ('ecp384bp', u'Group 29 ecp384bp'), ('ecp512bp', u'Group 30 ecp512bp')])

    esp_encryption_algorithm = SelectField(u'ESP 加密算法',
                                           choices=[('3des', u'3DES'), ('aes128', u'AES128'),
                                                    ('aes192', u'AES192'), ('aes256', u'AES256'),
                                                    ('aes128gcm64', u'AES128-GCM64'), ('aes192gcm64', u'AES192-GCM64'),
                                                    ('aes256gcm64', u'AES256-GCM64'), ('aes128gcm96', u'AES128-GCM96'),
                                                    ('aes192gcm96', u'AES192-GCM96'), ('aes256gcm96', u'AES256-GCM96'),
                                                    ('aes128gcm128', u'AES128-GCM128'), ('aes192gcm128', u'AES192-GCM128'),
                                                    ('aes256gcm128', u'AES256-GCM128')])

    esp_integrity_algorithm = SelectField(u'ESP 验证算法',
                                          choices=[('md5', u'MD5'), ('sha1', u'SHA1'),
                                                   ('sha2_256', u'SHA2-256'), ('sha2_384', u'SHA2-384'),
                                                   ('sha2_512', u'SHA2-512'), ('aesxcbc', u'AES-XCBC')])

    esp_dh_algorithm = SelectField(u'ESP DH 组',
                                   choices=[('null', u'无'),
                                            ('modp768', u'Group 1 modp768'), ('modp1024', u'Group 2 modp1024'),
                                            ('modp1536', u'Group 5 modp1536'), ('modp2048', u'Group 14 modp2048'),
                                            ('modp3072', u'Group 15 modp3072'), ('modp4096', u'Group 16 modp4096'),
                                            ('modp6144', u'Group 17 modp6144'), ('modp8192', u'Group 18 modp8192'),
                                            ('ecp256', u'Group 19 ecp256'), ('ecp384', u'Group 20 ecp384'),
                                            ('ecp521', u'Group 21 ecp521'), ('modp1024s160', u'Group 22 modp1024s160'),
                                            ('modp2048s224', u'Group 23 modp2048s224'), ('modp2048s256', u'Group 24 modp2048s256'),
                                            ('ecp192', u'Group 25 ecp192'), ('ecp224', u'Group 26 ecp224'),
                                            ('ecp224bp', u'Group 27 ecp224bp'), ('ecp256bp', u'Group 28 ecp256bp'),
                                            ('ecp384bp', u'Group 29 ecp384bp'), ('ecp512bp', u'Group 30 ecp512bp')])

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
