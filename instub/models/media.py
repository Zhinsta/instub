# -*- coding: utf-8 -*-

from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property

from instub.database import db, SurrogatePK, Model, redis


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

    workers = db.relationship(
        'Worker', lazy='select', backref='category',
        primaryjoin='Category.id==Worker.category_id',
        foreign_keys='Worker.category_id',
        uselist=True, passive_deletes='all')

    @hybrid_property
    def url(self):
        return url_for('category_view.category', name=self.name)

    def medias_query(self, category_id):
        query = (Media.query
                 .filter(Worker.category_id == category_id)
                 .filter(Worker.uid == Media.worker_id))
        return query

    def medias_count(self, category_id):
        key = 'media_count:%s' % category_id
        count = redis.get(key)
        if count:
            return int(count)
        query = self.medias_query(category_id)
        count = query.count()
        redis.setex(key, 3600, str(count))
        return count

    def medias(self, category_id, limit=20, offset=0):
        query = self.medias_query(category_id)
        medias = (query
                  .offset(offset).limit(limit)
                  .all())
        return medias


class Worker(SurrogatePK, Model):

    __tablename__ = 'worker'

    uid = db.Column(db.String(128), index=True, nullable=False, unique=True)
    category_id = db.Column(db.String(128), index=True, nullable=True, server_default='0')
    username = db.Column(db.String(128), index=True, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(64), nullable=True, index=True,
                       server_default='prepare')
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())
    updated_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())

    def __unicode__(self):
        return self.username if self.username else 'Unkonw'

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
    worker_id = db.Column(db.String(128), nullable=False)
    low_resolution = db.Column(db.String(256), nullable=False)
    thumbnail = db.Column(db.String(256), nullable=False)
    standard_resolution = db.Column(db.String(256), nullable=False)
    created_time = db.Column(db.DateTime(timezone=True),
                             index=True, nullable=False,
                             server_default=db.func.current_timestamp())

    @hybrid_property
    def url(self):
        return url_for('media_view.media', id=self.id)
