# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from md5 import md5

from flask_wtf import Form
from wtforms import TextField, HiddenField, StringField, widgets, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask.ext.login import current_user

from ..models import User


class LoginForm(Form):
    password = PasswordField('密码',
                             validators=[DataRequired(),
                                     Length(min=6, max=25)])
    email = TextField('邮箱',
                      validators=[DataRequired(),
                                  Email(),
                                  Length(min=6, max=40)])

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        password = md5('instub%s' % self.password.data).hexdigest()
        email = User.query.filter_by(email=self.email.data).first()
        if not email:
            self.email.errors.append("Email not registered")
            return False
        user = (User.query
                .filter_by(email=self.email.data,
                           password=password)
                .first())
        if not user:
            self.password.errors.append("Email or Password error")
            return False
        return True


class AddAdminForm(Form):
    name = StringField('昵称',
                       validators=[DataRequired(),
                                   Length(min=3, max=25)])
    mobile = StringField('电话',
                         validators=[DataRequired(),
                                     Length(min=11, max=16)])
    email = TextField('邮箱',
                      validators=[DataRequired(),
                                  Email(),
                                  Length(min=6, max=40)])
    password = PasswordField('密码',
                             validators=[DataRequired(),
                                     Length(min=6, max=25)])
    def validate(self):
        initial_validation = super(AddAdminForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(name=self.name.data).first()
        if user:
            self.nickname.errors.append("Username already registered")
            return False
        auth = User.query.filter_by(email=self.email.data).first()
        if auth:
            self.email.errors.append("Email already registered")
            return False
        return True
