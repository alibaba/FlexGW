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
from wtforms.validators import DataRequired, Length

from website.account.models import User


class LoginForm(Form):
    account = TextField(u'Account', validators=[DataRequired(message=u'这是一个必选项！'),
                                                Length(max=20, message=u'帐号最长为20个字符！')])
    password = PasswordField(u'Password', validators=[DataRequired(message=u'这是一个必选项！')])

    def validate_password(self, field):
        account = self.account.data
        if not User.check_auth(account, field.data):
            raise ValidationError(u'无效的帐号或密码！')
