# coding: utf-8

import gevent
from gevent.queue import Queue, Empty
from gevent import monkey
gevent.monkey.patch_all()

from jinja2 import Markup
from flask import url_for
from flask import request
from flask import redirect
from flask import flash
from flask.ext.login import (login_required, current_user,
                             login_user, logout_user)
from flask.ext.admin import helpers, expose, AdminIndexView
from flask.ext.admin.babel import gettext, ngettext, lazy_gettext
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla.tools import get_query_for_ids
from flask.ext.admin.actions import action

from instagram import InstagramAPI
from instagram import InstagramAPIError

from instub.database import (db, get_fresh_worker, get_last_media,
                             get_token, insert_medias, set_worker_done,
                             set_worker_prepare, update_worker, delete_worker)
from instub.models import Category, Worker, User, Media
from instub.errors import NotFound, InternalServerError
from instub.utils import update_workers

from .forms import LoginForm

tasks = Queue(maxsize=3)


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
        return medias_list
    except InstagramAPIError, e:
        if e.error_type in ['APINotAllowedError-you',
                            'APINotFoundError-this']:
            delete_worker(uid)
        return InternalServerError(u'服务器暂时出问题了')


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

    def _update_worker(self):
        try:
            task = tasks.get(timeout=1)
            uid = get_fresh_worker(fetchone=True)
            if not uid:
                return
            access_token = get_token(fetchone=True)
            if not access_token:
                return
            min_id = get_last_media(uid=uid)
            medias = get_medias(uid=uid, access_token=access_token,
                                      min_id=min_id)
            if medias:
                insert_medias(medias[:-1])
                if isinstance(medias, list):
                    worker = medias[0].user
                    update_worker(uid, worker.username, worker.profile_picture)
            set_worker_done(uid)
            gevent.sleep(0)
        except Empty:
            print 'ALL DONE'

    def _put_tasks(self, total):
        for i in xrange(0, total):
            tasks.put(i)
        print 'total: %s DONE' % total

    @expose('/update_workers_media')
    def update_workers_media(self):
        total = Worker.query.count()
        set_worker_prepare()
        gevent.spawn(self._put_tasks, total=total)
        fs = []
        for i in xrange(0, min(1, total)):
            g = gevent.spawn(self._update_worker)
            fs.append(g)
        gevent.joinall(fs)
        return super(PanelIndex, self).index()

    @expose('/update_workers')
    def update_workers(self):
        update_workers()
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

    #column_list = ('uid', Category.name, 'username', 'profile_picture',
    #               'status', 'created_time', 'updated_time')
    # Visible columns in the list view
    column_exclude_list = ['category_id']

    # List of columns that can be sorted.
    column_sortable_list = ('uid', 'username', 'created_time',
                            'updated_time')

    # Rename 'title' columns to 'Post Title' in list view
    column_labels = dict(username='Username',
                         profile_picture='Avatar')

    column_searchable_list = ('username',  Category.name)

    column_filters = ('username',
                      Category.name,
                      'created_time')

    def _show_pic(self, context, model, name):
        return Markup('<img src=%s width=90 height=90>' % model.profile_picture)

    def _show_user(self, context, model, name):
        return Markup('<a href="%s">%s</a>' % (
            url_for('user_view.profile', uid=model.uid),
            model.username))

    def _update_worker(self, uid):
        access_token = get_token(fetchone=True)
        if not access_token:
            return
        min_id = get_last_media(uid=uid)
        medias = get_medias(uid=uid, access_token=access_token,
                                  min_id=min_id)
        if medias:
            insert_medias(medias[:-1])
            if isinstance(medias, list):
                worker = medias[0].user
                update_worker(uid, worker.username, worker.profile_picture)
        set_worker_done(uid)

    @action('refresh', lazy_gettext('Refresh'),
            lazy_gettext(u'手动更新，不要超过5个'))
    def action_refresh(self, ids):
        try:
            query = get_query_for_ids(self.get_query(), self.model, ids)
            for worker in query.all():
                self._update_worker(worker.uid)
            count = query.count()
            flash(ngettext('Record was successfully refreshed.',
                           '%(count)s records were successfully refreshed.',
                           count, count=count))
        except Exception as ex:
            flash(gettext('Failed to refresh records. %(error)s',
                          error=str(ex)), 'error')

    column_formatters = {
        'username': _show_user,
        'profile_picture': _show_pic,
    }

    def __init__(self, **kwargs):
        super(WorkerPanel, self).__init__(Worker, db.session, **kwargs)


class MediaPanel(PanelBase):

    column_list = ('id', 'worker_id', 'low_resolution', 'thumbnail',
                   'standard_resolution', 'created_time')
    column_searchable_list = ('id', 'worker_id')
    column_sortable_list = ('id', 'created_time')
    column_filters = ('id',
                      Worker.username,
                      'created_time')

    def _show_low(self, context, model, name):
        return Markup('<img src=%s width=90 height=90>' % model.low_resolution)

    def _show_thumbnail(self, context, model, name):
        return Markup('<img src=%s width=90 height=90>' % model.thumbnail)

    def _show_standard(self, context, model, name):
        return Markup('<img src=%s width=90 height=90>' % model.standard_resolution)

    column_formatters = {
        'low_resolution': _show_low,
        'thumbnail': _show_thumbnail,
        'standard_resolution': _show_standard,
    }

    def __init__(self, **kwargs):
        super(MediaPanel, self).__init__(Media, db.session, **kwargs)
