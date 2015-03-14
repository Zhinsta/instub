# -*- coding: utf-8 -*-

from functools import wraps

import gevent
from gevent.util import wrap_errors
from flask import render_template, session, request, redirect, url_for
from flask.ext.login import LoginManager

from instagram import InstagramAPIError, InstagramAPI

from instub.database import get_token

login_manager = LoginManager()


def open_visit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if has_login():
            request.access_token = session['access_token']
        else:
            request.access_token = get_token(fetchone=True)
        request.uid = None
        return func(*args, **kwargs)
    return wrapper


def has_login():
    if not session.get('uid', ''):
        return False
    if not session.get('access_token', ''):
        return False
    if not session.get('username', ''):
        return False
    return True


def online_user():
    if has_login():
        from instub.models import User
        user = User.query.get(session['uid'])
        if not user:
            return False
        return user
    return


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not has_login():
            if not request.access_token:
                return redirect(url_for('views.login'))
        else:
            request.uid = session['uid']
            request.access_token = session['access_token']
        return func(*args, **kwargs)
    return wrapper


def spawn(fn, *args, **kwargs):
    return gevent.spawn(wrap_errors(InstagramAPIError, fn), *args, **kwargs)


def isfollow(uid, api=None):
    if not api:
        api = InstagramAPI(access_token=session.get('access_token', ''))
        data = api.user_relationship(user_id=uid)
        if data.outgoing_status == 'follows':
            return True
    return False


def render(template, **argkv):
    uid = ''
    if request.uid:
        uid = request.uid
    if uid:
        argkv.update({'has_login': True,
                      'username': session.get('username', ''),
                      'uid': uid,
                      'request': request})
    else:
        argkv.update({'has_login': False})
    return render_template(template, **argkv)


def apierror(message=None, status_code=500):
    if not message:
        message = \
            u'服务器不给力，勇敢的少年啊，请重新试一次吧'
    return (render('error.html', message=message), status_code)


def get_errors(*rs):
    return [e for e in rs if isinstance(e, InstagramAPIError)]


def all_categories():
    from instub.models import Category
    categories = Category.query.order_by(Category.sort_score.desc()).all()
    return categories


def site_setting():
    from instub.models import SiteSetting
    setting = SiteSetting.query.first()
    return setting


def get_workers():
    import os
    import csv
    current_path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(current_path, 'data')
    workers_file = []
    for filename in os.listdir(data_path):
        if '.csv' in filename:
            workers_file.append(filename)
    workers_dict = {}
    for wfile in workers_file:
        filepath = os.path.join(data_path, wfile)
        category = wfile.split('.')[0]
        cworkers = []
        with open(filepath, 'rb') as workers:
            reader = csv.reader(workers, delimiter=',', quotechar='|')
            for url in reader:
                if url and url[0]:
                    url_split = url[0].split('/')
                    if len(url_split) > 2:
                        uid = url_split[-2]
                        if uid.isdigit():
                            cworkers.append(uid)
        workers_dict[category] = cworkers
    return workers_dict


def update_workers():
    from instub.models import Category, Worker
    workers = get_workers()
    for category_name in workers:
        category = Category.query.filter(Category.name == category_name).first()
        if not category:
            category = Category.create(name=category_name, key=category_name)
        uids = workers.get(category_name)
        for uid in uids:
            worker = Worker.query.filter(Worker.uid == uid).first()
            if not worker:
                worker = Worker.create(uid=uid, category_id=category.id)
