# coding: utf-8

from flask import url_for
from flask import request
from flask import redirect
from flask.ext.login import (login_required, current_user,
                             login_user, logout_user)
from flask.ext.admin import helpers, expose, AdminIndexView
from flask.ext.admin.contrib import sqla

from instub.models import Category, Worker

from .forms import LoginForm


class PanelBase(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated()


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


class SitePanel(PanelBase):
    pass


class UserPanel(PanelBase):
    pass


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
