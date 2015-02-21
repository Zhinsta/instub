# coding: utf-8

import gevent

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

from instub.database import db
from instub.models import Category, Worker, User, Media
from instub.errors import NotFound, InternalServerError

from .forms import LoginForm


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

    def _get_token(self):
        count = User.query.count()
        import random
        offset = random.randint(0, count - 1) if count > 1 else 0
        user = User.query.offset(offset).first()
        return user.access_token

    def _get_medias(self, user, access_token, last_media=None):
        api = InstagramAPI(access_token=access_token)
        next_ = True
        medias_list = []
        while next_:
            next_url = None if next_ is True else next_
            if last_media:
                medias, next_ = api.user_recent_media(
                    user_id=user.uid, with_next_url=next_url,
                    min_id=last_media.mid)
            else:
                medias, next_ = api.user_recent_media(
                    user_id=user.uid, with_next_url=next_url)
            medias_list.extend(medias)
        return medias_list

    def _update_workers(self, users):
        print '*' * 100
        print users
        users_list = []
        for user in users:
            access_token = self._get_token()
            last_media = (Media.query
                          .filter(Media.worker_id == user.uid)
                          .order_by(Media.created_time.desc()).first())
            user = gevent.spawn(
                self._get_medias, user=user,
                access_token=access_token, last_media=last_media)
            users_list.append(user)

        try:
            gevent.joinall(users_list)
        except InstagramAPIError:
            return InternalServerError(u'服务器暂时出问题了')
        for user in users_list:
            medias = user.value
            if medias:
                for media in medias[:-1]:
                    Media.create(
                        mid=media.id,
                        worker_id=media.user.id,
                        low_resolution=media.images['low_resolution'],
                        thumbnail=media.images['thumbnail'],
                        standard_resolution=media.images['standard_resolution'],
                        created_time=media.created_time)

    @expose('/update_worker')
    def update_workers_media(self):
        total = Worker.query.count()
        offset = 0
        limit = 50
        for i in xrange(offset, total, limit):
            workers = (
                Worker.query.order_by(Worker.updated_time)
                .offset(offset).limit(limit).all())
            self._update_workers(workers)
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

    column_sortable_list = ('mid', 'created_time')
    column_filters = ('mid',
                      Worker.user_name,
                      'created_time')
