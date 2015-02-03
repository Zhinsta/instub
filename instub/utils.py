# -*- coding: utf-8 -*-

from functools import wraps

from flask import render_template, session
from flask.ext.login import LoginManager

login_manager = LoginManager()


def has_login():
    from instub.models import User
    if not session.get('uid', ''):
        return False
    if not session.get('access_token', ''):
        return False
    if not session.get('username', ''):
        return False
    user = UserModel.query.get(session['uid'])
    if not user:
        return False
    return user


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



def render(template, **argkv):
    uid = ''
    if request.uid:
        uid = request.uid
    if ukey:
        argkv.update({'has_login': True,
                      'username': session.get('username', ''),
                      'uid': ukey,
                      'request': request})
    else:
        argkv.update({'has_login': False})
    return render_template(template, **argkv)


def apierror(message=None, status_code=500):
    if not message:
        message = \
            u'服务器不给力，勇敢的少年啊，请重新试一次吧'
    return (render('error.html', message=message), status_code)
