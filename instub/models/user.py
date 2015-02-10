# -*- coding: utf-8 -*-

from flask.ext.login import UserMixin
from instub.database import db, SurrogatePK, Model

from instub.utils import login_manager


@login_manager.user_loader
def get_user(id):
    admin = iAdmin.query.get(id)
    return admin


class SiteSetting(SurrogatePK, Model):

    __tablename__ = 'site_setting'

    name = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    keyword = db.Column(db.String(255), nullable=False)
    slogan = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())


class User(SurrogatePK, Model):

    __tablename__ = 'user'

    name = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())


class iAdmin(UserMixin, SurrogatePK, Model):

    __tablename__ = 'admin'
    __table_args__ = (
        db.Index('ix_admin_email_password', 'email', 'password'),
    )

    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    mobile = db.Column(db.String(128), nullable=True)
    password = db.Column(db.String(128), nullable=False)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())
