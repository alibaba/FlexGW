# -*- coding: utf-8 -*-
"""
    website.account.forms
    ~~~~~~~~~~~~~~~~~~~~~

    account forms:
        /login
        /settings

    :copyright: (c) 2014 by xiong.xiaox(xiong.xiaox@alibaba-inc.com).
"""


from flask_wtf import Form
from wtforms import TextField, PasswordField, ValidationError
from wtforms.validators import Required, Length, EqualTo

from website.account.models import User


class LoginForm(Form):
    account = TextField('Account', validators=[Required(), Length(max=20, message=u'帐号最长为20个字符！')])
    password = PasswordField('Password', validators=[Required()])

    def validate_password(self, field):
        account = self.account.data
        user = User.query.filter_by(account=account).first()
        if not user or not user.check_password(field.data):
            raise ValidationError(u'无效的帐号或密码！')


class SettingsForm(Form):
    password = PasswordField('New Password', [Required(), EqualTo('confirm', message=u'两次密码不匹配！')])
    confirm = PasswordField('Repeat Password')
