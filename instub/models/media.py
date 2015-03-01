# -*- coding: utf-8 -*-

from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property

from instub.database import db, SurrogatePK, Model


class Category(SurrogatePK, Model):

    __tablename__ = 'category'

    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    key = db.Column(db.String(128), index=True, nullable=True, unique=True)
    sort_score = db.Column(db.Integer(), index=True, nullable=True)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())

    def __unicode__(self):
        return self.name

    @hybrid_property
    def url(self):
        return url_for('category_view.category', name=self.name)

    def medias_query(self):
        query = (Media.query
                 .filter(Category.id == self.id)
                 .filter(Category.id == WorkerCategory.category_id)
                 .filter(Worker.id == WorkerCategory.worker_id)
                 .filter(Worker.uid == Media.worker_id))
        return query

    def medias_count(self):
        query = self.medias_query()
        return query.count()

    def medias(self, limit=20, offset=0):
        query = self.medias_query()
        medias = (query
                  .order_by(Media.created_time.desc())
                  .offset(offset).limit(limit)
                  .all())
        return medias

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

    uid = db.Column(db.String(128), index=True, nullable=False, unique=True)
    user_name = db.Column(db.String(128), index=True, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(64), nullable=False, index=True,
                       server_default='prepare')
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


class WorkerCategory(Model):

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

    @hybrid_property
    def url(self):
        return 'test'
        #return url_for('media_view.profile', id=self.id)
