# coding: utf-8

import gevent
from gevent.queue import Queue, Empty
from gevent import monkey
gevent.monkey.patch_all()

from jinja2 import Markup
from flask import url_for
from flask import request
from flask import redirect
from flask.ext.login import (login_required, current_user,
                             login_user, logout_user)
from flask.ext.admin import helpers, expose, AdminIndexView
from flask.ext.admin.contrib import sqla

from instagram import InstagramAPI
from instagram import InstagramAPIError

from instub.database import (db, get_fresh_worker, get_last_media,
                             get_token, insert_medias, set_worker_done,
                             set_worker_prepare)
from instub.models import Category, Worker, User, Media
from instub.errors import NotFound, InternalServerError

from .forms import LoginForm

tasks = Queue(maxsize=3)


class PanelBase(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated()

    def is_text_column_type(self, name):
        if name:
            name = name.lower()
        return name in ('string', 'unicode', 'text', 'unicodetext', 'varchar')


class PanelIndex(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(PanelIndex, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated():
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(PanelIndex, self).index()

    @expose('/logout/')
    def logout(self):
        logout_user()
        return redirect(url_for('.index'))

    def _get_medias(self, uid, access_token, min_id=None):
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
            return medias_list
        except InstagramAPIError:
            return InternalServerError(u'服务器暂时出问题了')

    def _update_worker(self):
        task = tasks.get(timeout=1)
        uid = get_fresh_worker(fetchone=True)
        if not uid:
            return
        access_token = get_token(fetchone=True)
        if not access_token:
            return
        min_id = get_last_media(uid=uid)
        medias = self._get_medias(uid=uid, access_token=access_token,
                                  min_id=min_id)
        if medias:
            insert_medias(medias[:-1])
        set_worker_done(uid)

    def _put_tasks(self, total):
        for i in xrange(0, total):
            tasks.put(i)
        print 'total: %s DONE' % total

    @expose('/update_worker')
    def update_workers_media(self):
        total = Worker.query.count()
        set_worker_prepare()
        gevent.spawn(self._put_tasks, total=total)
        fs = []
        for i in xrange(0, min(50, total)):
            g = gevent.spawn(self._update_worker)
            fs.append(g)
        gevent.joinall(fs)
        return super(PanelIndex, self).index()


class SitePanel(PanelBase):
    pass


class UserPanel(PanelBase):

    column_list = ('id', 'name', 'avatar', 'created_time')
    column_searchable_list = ('name', 'id')
    column_filters = ('created_time',)

    def _show_pic(self, context, model, name):
        return Markup('<img src=%s width=90 height=90>' % model.avatar)

    def _show_user(self, context, model, name):
        return Markup('<a href="%s">%s</a>' % (
            url_for('user_view.profile', uid=model.id),
            model.name))

    column_formatters = {
        'name': _show_user,
        'avatar': _show_pic,
    }

    def __init__(self, **kwargs):
        super(UserPanel, self).__init__(User, db.session, **kwargs)


class AdminPanel(PanelBase):
    pass


class CategoryPanel(PanelBase):
    pass


class WorkerPanel(PanelBase):

    # Visible columns in the list view
    column_exclude_list = []

    # List of columns that can be sorted.
    column_sortable_list = ('user_name', 'full_name', 'created_time',
                            'updated_time')

    # Rename 'title' columns to 'Post Title' in list view
    column_labels = dict(user_name='Username',
                         full_name='Fullname',
                         profile_picture='Avatar')

    column_searchable_list = ('user_name', 'full_name', Category.name)

    column_filters = ('user_name',
                      'full_name',
                      Category.name,
                      'created_time')


class MediaPanel(PanelBase):

    column_sortable_list = ('id', 'created_time')
    column_filters = ('id',
                      Worker.user_name,
                      'created_time')
