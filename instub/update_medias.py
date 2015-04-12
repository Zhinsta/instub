# coding: utf-8

import random
import optparse

import gevent
from gevent.queue import Queue, Empty
from gevent import monkey
gevent.monkey.patch_all()
import MySQLdb
from functools import wraps

from instagram import InstagramAPI
from instagram import InstagramAPIError

tasks = Queue(maxsize=10)
parser = optparse.OptionParser()
parser.add_option('-t', '--total',
                  dest='worker_total',
                  type="int")
options, args = parser.parse_args()


class Configuraion:
    def __init__(self):
        import settings
        self.db = settings.DB_DATEBASE
        self.host = settings.DB_HOST
        self.port = settings.DB_PORT
        self.user = settings.DB_USER
        self.passwd = settings.DB_PASSWORD


def mysql(sql, param=None, op='query'):

    _conf = Configuraion()

    def on_sql_error(err):
        # import sys
        print '---------------------'
        print err
        if err[0] == 1062:
            mid = err[1].split("'")[1]
            delete_media(mid)
        print '---------------------'
        # sys.exit(-1)

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
@mysql(sql='select uid, username from worker order by updated_time limit 1')
def get_fresh_worker(data, fetchone=True):
    if data:
        uid = data[0]
        sql = 'update worker set status="doing" where uid="%s"' % uid
        execute_sql(sql, op='update')
        return uid
    return


def get_worker(uid, fetchone=True):
    sql = 'select uid, username from worker where uid="%s"' % uid

    @mysql(sql=sql)
    def execute(data, fetchone=True):
        if data:
            uid, username = data
            return uid, username
        return None, None

    return execute(fetchone=fetchone)


def set_worker_prepare():
    sql = 'update worker set status="prepare"'
    execute_sql(sql, op='update')


def set_worker_done(uid):
    from datetime import datetime
    now = datetime.now()
    sql = 'update worker set status="done", updated_time="%s" where uid="%s"' % (now, uid)
    execute_sql(sql, op='update')


def update_worker(uid, username, profile_picture):
    print uid, username, profile_picture
    sql = ('update worker set username="%s", '
           'profile_picture="%s" where uid="%s"' %
           (username, profile_picture, uid))
    execute_sql(sql, op='update')


def delete_worker(uid):
    sql = 'delete from worker where uid="%s"' % uid
    execute_sql(sql, op='delete')


def delete_media(id):
    sql = 'delete from media where id="%s"' % id
    print 'delete:%s' % id
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
    print '*' * 100
    if param:
        print param[0][1]
    execute_sql(sql, param, op='insert')


def get_medias(uid, access_token, min_id=None):
    print uid, access_token, min_id
    try:
        api = InstagramAPI(access_token=access_token)
        medias_list = []
        next_ = True
        while next_:
            next_url = None if next_ is True else next_
            medias, next_ = api.user_recent_media(
                user_id=uid, with_next_url=next_url,
                min_id=min_id)
            medias_list.extend(medias)
        print len(medias_list)
        return medias_list
    except InstagramAPIError, e:
        if e.error_type in ['APINotAllowedError-you',
                            'APINotFoundError-this']:
            delete_worker(uid)
            print e.error_type
        return e


def get_user(uid, access_token):
    try:
        api = InstagramAPI(access_token=access_token)
        user = api.user(uid)
        return user
    except InstagramAPIError, e:
        if e.error_type in ['APINotAllowedError-you',
                            'APINotFoundError-this']:
            delete_worker(uid)
            print e.error_type
        return e


def _update_worker(worker_num):
    while not tasks.empty():
        task = tasks.get(timeout=1)
        print('Worker %s got task %s' % (worker_num, task))
        try:
            uid = get_fresh_worker(fetchone=True)
            if not uid:
                return
            print "uid: %s" % uid
            access_token = get_token(fetchone=True)
            if not access_token:
                return
            min_id = get_last_media(uid=uid)
            print "min_id: %s" % min_id
            medias = get_medias(uid=uid, access_token=access_token, min_id=min_id)
            if medias:
                insert_medias(medias[:-1])
                if isinstance(medias, list):
                    worker = medias[0].user
                    update_worker(uid, worker.username, worker.profile_picture)
                else:
                    username = get_worker(uid)
                    print "username: %s " % username
                    if not username:
                        user = get_user(uid)
                        print type(user)
                        update_worker(uid, user.username, user.profile_picture)
            set_worker_done(uid)
            gevent.sleep(random.randint(1, 10))
        except Empty:
            print 'ALL DONE'


def _put_tasks(total):
    for i in xrange(0, total):
        tasks.put(i)
    print 'total: %s DONE' % total


def update_workers_media(total=20):
    set_worker_prepare()
    gevent.spawn(_put_tasks, total=total)
    fs = []
    for i in xrange(0, min(20, 5)):
        g = gevent.spawn(_update_worker, worker_num=i)
        fs.append(g)
    gevent.joinall(fs)


if __name__ == '__main__':
    total = options.worker_total
    if not total:
        total = 20
    update_workers_media(total)
