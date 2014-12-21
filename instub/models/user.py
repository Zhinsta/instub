# -*- coding: utf-8 -*-

from flask.ext.login import UserMixin
from instub.database import db, SurrogatePK, Model

from instub.utils import login_manager


@login_manager.user_loader
def get_user(id):
    admin = Admin.query.get(int(id))
    return admin


class SiteSetting(SurrogatePK, Model):

    __tablename__ = 'site_setting'

    name = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    keywords = db.Column(db.String(255), nullable=False)
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


class Admin(UserMixin, SurrogatePK, Model):

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


class Category(SurrogatePK, Model):

    __tablename__ = 'category'

    name = db.Column(db.String(128), nullable=False)
    key = db.Column(db.String(128), index=True, nullable=True)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())

    @classmethod
    def __declare_last__(cls):
        cls.workers = db.relationship(
            'Worker',
            secondary=WorkerCategory.__table__,
            backref=db.backref(
                'categories',
                innerjoin=True,
                order_by=Worker.created_time.desc(),
                lazy='dynamic',),
            primaryjoin=cls.id == WorkerCategory.category_id,
            secondaryjoin=WorkerCategory.worker_id == Worker.id,
            order_by=WorkerCategory.created_time.desc(),
            foreign_keys=[WorkerCategory.category_id, WorkerCategory.worker_id],
            passive_deletes='all', lazy='dynamic')


class Worker(Model):

    __tablename__ = 'worker'

    id = db.Column(db.String(128), primary_key=True, autoincrement=False)
    user_name = db.Column(db.String(128), index=True, nullable=False)
    full_name = db.Column(db.String(128), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())
    updated_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())


class WorkerCategory(Model):

    __tablename__ = 'worker_category'

    worker_id = db.Column(db.String(128), primary_key=True)
    category_id = db.Column(db.String(128), primary_key=True)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())


class Media(Model):

    __tablename__ = 'media'

    mid = db.Column(db.String(128), primary_key=True, autoincrement=False)
    worker_id = db.Column(db.String(128), nullable=False, index=True)
    low_resolution = db.Column(db.String(256), nullable=False)
    thumbnail = db.Column(db.String(256), nullable=False)
    standard_resolution = db.Column(db.String(256), nullable=False)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())
    updated_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())
