# -*- coding: utf-8 -*-

from flask.ext.login import UserMixin
from instub.database import db, SurrogatePK, Model


class Category(SurrogatePK, Model):

    __tablename__ = 'category'

    name = db.Column(db.String(128), nullable=False)
    key = db.Column(db.String(128), index=True, nullable=True)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())

    def __unicode__(self):
        return self.name

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


class Worker(SurrogatePK, Model):

    __tablename__ = 'worker'

    uid = db.Column(db.String(128), index=True, nullable=False)
    user_name = db.Column(db.String(128), index=True, nullable=False)
    full_name = db.Column(db.String(128), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(64), nullable=False, index=True)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())
    updated_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())

    medias = db.relationship(
        'Media', lazy='select', backref='worker',
        primaryjoin='Worker.uid==Media.worker_id',
        foreign_keys='Media.worker_id',
        uselist=True, passive_deletes='all')


class WorkerCategory(SurrogatePK, Model):

    __tablename__ = 'worker_category'

    worker_id = db.Column(db.String(128), primary_key=True)
    category_id = db.Column(db.String(128), primary_key=True)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())


class Media(Model):

    __tablename__ = 'media'

    id = db.Column(db.String(128), index=True, primary_key=True,
                   autoincrement=False, nullable=False)
    worker_id = db.Column(db.String(128), nullable=False, index=True)
    low_resolution = db.Column(db.String(256), nullable=False)
    thumbnail = db.Column(db.String(256), nullable=False)
    standard_resolution = db.Column(db.String(256), nullable=False)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())
