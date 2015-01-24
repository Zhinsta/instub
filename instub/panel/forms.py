# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from md5 import md5

from flask_wtf import Form
from wtforms import TextField, HiddenField, StringField, widgets, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask.ext.login import current_user

from ..models import iAdmin


class LoginForm(Form):
    email = TextField('email',
                      validators=[DataRequired(),
                                  Email(),
                                  Length(min=6, max=40)])
    password = PasswordField('password',
                             validators=[DataRequired(),
                                         Length(min=6, max=25)])

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        password = md5('instub%s' % self.password.data).hexdigest()
        email = iAdmin.query.filter_by(email=self.email.data).first()
        if not email:
            self.email.errors.append("Email not registered")
            return False
        user = (iAdmin.query
                .filter_by(email=self.email.data,
                           password=password)
                .first())
        if not user:
            self.password.errors.append("Email or Password error")
            return False
        return True

    def get_user(self):
        return iAdmin.query.filter(iAdmin.email == self.email.data).first()


class AddAdminForm(Form):
    name = StringField('nickname',
                       validators=[DataRequired(),
                                   Length(min=3, max=25)])
    mobile = StringField('mobile',
                         validators=[DataRequired(),
                                     Length(min=11, max=16)])
    email = TextField('email',
                      validators=[DataRequired(),
                                  Email(),
                                  Length(min=6, max=40)])
    password = PasswordField('password',
                             validators=[DataRequired(),
                                         Length(min=6, max=25)])

    def validate(self):
        initial_validation = super(AddAdminForm, self).validate()
        if not initial_validation:
            return False
        user = iAdmin.query.filter_by(name=self.name.data).first()
        if user:
            self.nickname.errors.append("Adminname already registered")
            return False
        auth = iAdmin.query.filter_by(email=self.email.data).first()
        if auth:
            self.email.errors.append("Email already registered")
            return False
        return True


class EditAdminForm(Form):
    name = StringField('nickname',
                       validators=[DataRequired(),
                                   Length(min=3, max=25)])
    mobile = StringField('mobile',
                         validators=[DataRequired(),
                                     Length(min=11, max=16)])
    email = TextField('email',
                      validators=[DataRequired(),
                                  Email(),
                                  Length(min=6, max=40)])
    password = PasswordField('password',
                             validators=[DataRequired(),
                                         Length(min=6, max=25)])

    def validate(self):
        initial_validation = super(EditAdminForm, self).validate()
        if not initial_validation:
            return False
        user = (iAdmin.query
                .filter(iAdmin.name == self.name.data)
                .filter(iAdmin.id != current_user.id)
                .first())
        if user:
            self.nickname.errors.append("Adminname already registered")
            return False
        auth = (iAdmin.query
                .filter(iAdmin.email == self.email.data)
                .filter(iAdmin.id != current_user.id)
                .first())
        if auth:
            self.email.errors.append("Email already registered")
            return False
        return True


class CategoryEditForm(Form):
    name = StringField('name',
                       validators=[DataRequired(),
                                   Length(min=3, max=25)])
    key = StringField('key', validators=[DataRequired(), Length(min=3, max=25)])
