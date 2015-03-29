# -*- coding: utf-8 -*-
"""
Database module, including the SQLAlchemy database object and DB-related
utilities.
"""
import random
from functools import wraps

import redis
import MySQLdb
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, TypeDecorator, Text
from flask import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

from instub.settings import REDIS_URL

redis = redis.StrictRedis.from_url(REDIS_URL)

db = SQLAlchemy()
migrate = Migrate()

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship


def generat_id():
    id = random.randint(17592186044416, 281474976710655)
    return hex(id)[2:]


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(128), primary_key=True, autoincrement=False,
                   default=generat_id)

    @classmethod
    def get_by_id(cls, id):
        # if any(
        #     (isinstance(id, basestring) and id.isdigit(),
        #      isinstance(id, (int, float))),
        # ):
        #     return cls.query.get(int(id))
        # return None
        return cls.query.get(id)


def ReferenceCol(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = ReferenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
        nullable=nullable, **kwargs)


class JsonString(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        return JsonString(self.impl.length)


class JsonText(JsonString):
    impl = Text

    def copy(self):
        return JsonText(self.impl.length)


class Configuraion:
    def __init__(self):
        from instub import settings
        self.db = settings.DB_DATEBASE
        self.host = settings.DB_HOST
        self.port = settings.DB_PORT
        self.user = settings.DB_USER
        self.passwd = settings.DB_PASSWORD


def mysql(sql, param=None, op='query'):

    _conf = Configuraion()

    def on_sql_error(err):
        #import sys
        print '---------------------'
        print err
        print '---------------------'
        #sys.exit(-1)

    def handle_sql_result(cursor, is_fetchone):
        if is_fetchone:
            ver = cursor.fetchone()
        else:
            ver = cursor.fetchall()
        return ver

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            is_fetchone = kwargs.get('fetchone', None)
            conn = MySQLdb.connect(host=_conf.host, port=_conf.port,
                                   user=_conf.user, passwd=_conf.passwd,
                                   db=_conf.db, charset="utf8")
            cursor = conn.cursor()
            try:
                if param and isinstance(param, list) and len(param) > 1:
                    cursor.executemany(sql, param)
                elif param:
                    cursor.execute(sql, param[0])
                else:
                    cursor.execute(sql)
            except MySQLdb.DatabaseError as e:
                on_sql_error(e)

            if op == 'query':
                data = handle_sql_result(cursor, is_fetchone)
            elif op in ['insert', 'update', 'delete']:
                data = []
                conn.commit()
            result = fn(data, **kwargs)
            cursor.close()
            conn.close()
            return result
        return wrapper

    return decorator


def yield_param(param):
    limit = 1000
    offset = 0
    total = len(param)

    while total > offset:
        result = param[offset: offset + limit]
        offset += limit
        yield result


def execute_sql(sql, param=None, op='query'):

    def _execute(sql, param=None, op=op):
        @mysql(sql, param=param, op=op)
        def execute(data):
            return data
        execute()

    if isinstance(param, list):
        for p in yield_param(param):
            _execute(sql, param=p, op=op)
    elif isinstance(param, tuple):
        _execute(sql, param=param, op=op)
    else:
        _execute(sql, op=op)
    return


@mysql(sql='select access_token from user order by rand() limit 1')
def get_token(data, fetchone=True):
    if data:
        token = data[0]
        return token
    return


# 从最老的开始更新 忽略状态
@mysql(sql='select uid from worker order by updated_time limit 1')
def get_fresh_worker(data, fetchone=True):
    if data:
        uid = data[0]
        sql = 'update worker set status="doing" where uid="%s"' % uid
        execute_sql(sql, op='update')
        return uid
    return


def set_worker_prepare():
    sql = 'update worker set status="prepare" where status="done"'
    execute_sql(sql, op='update')


def set_worker_done(uid):
    from datetime import datetime
    now = datetime.now()
    sql = 'update worker set status="done", updated_time="%s" where uid="%s"' % (now, uid)
    execute_sql(sql, op='update')


def update_worker(uid, username, profile_picture):
    sql = ('update worker set username="%s", '
           'profile_picture="%s" where uid="%s"' %
           (username, profile_picture, uid))
    execute_sql(sql, op='update')


def delete_worker(uid):
    sql = 'delete from worker where uid="%s"' % uid
    execute_sql(sql, op='delete')


def get_last_media(uid, fetchone=True):
    sql = ('select id from media where worker_id="%s" '
           'order by created_time desc limit 1' % uid)

    @mysql(sql=sql)
    def execute(data, fetchone=True):
        if data:
            mid = data[0]
            return mid
        return

    return execute(fetchone=fetchone)


def insert_medias(medias):
    sql = ("insert into media(id, worker_id, low_resolution, thumbnail, "
           "standard_resolution, created_time) values(%s, %s, %s, %s, %s, %s)")
    param = [(media.id, media.user.id,
              media.images['low_resolution'],
              media.images['thumbnail'],
              media.images['standard_resolution'],
              media.created_time) for media in medias]
    execute_sql(sql, param, op='insert')
