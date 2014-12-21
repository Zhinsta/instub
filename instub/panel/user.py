# coding: utf-8

from flask import views
from flask import url_for
from flask import redirect
from flask import render_template
from flask.ext.login import login_required, current_user

from instub.models import Category, Worker
from instub.utils import notfound
from instub.pager import Pager

from .forms import CategoryEditForm


class Categories(views.MethodView):

    template = '/panel/categories.html'

    @login_required
    def get(self, id=None):
        if id:
            self.template = '/panel/category.html'
            category = Category.query.get(id)
            if not category:
                return notfound('category not exists')
            query = category.workers
            print query
            pager = Pager(query.count())
            workers = (query.order_by(Worker.created_time.desc())
                       .offset(pager.offset)
                       .limit(pager.per_page)
                       .all())
            return render_template(self.template, category=category,
                                   workers=workers, pager=pager)
        query = Category.query
        pager = Pager(query.count())
        categories = (query.order_by(Category.created_time.desc())
                      .offset(pager.offset).limit(pager.per_page)
                      .all())
        return render_template(self.template, categories=categories,
                               pager=pager)


class CategoryEdit(views.MethodView):

    template = '/panel/category_edit.html'

    @login_required
    def get(self, id=None):
        if id:
            category = Category.query.get(id)
            if not category:
                return notfound('category not found')
            form = CategoryEditForm(name=category.name,
                                    key=category.key)
        else:
            form = CategoryEditForm()
        return render_template(self.template, form=form)

    def category_add(self):
        form = CategoryEditForm()
        if form.validate_on_submit():
            Category.create(name=form.name.data,
                            key=form.key.data)
            return redirect(url_for('panel.categories'))
        return render_template(self.template, form=form)

    def category_edit(self, id):
        category = Category.query.get(id)
        if not category:
            return notfound('category not found')
        form = CategoryEditForm()
        if form.validate_on_submit():
            category.update(name=form.name.data,
                            key=form.key.data)
            return redirect(url_for('panel.category', id=id))
        return render_template(self.template, form=form)

    @login_required
    def post(self, id=None):
        if id:
            return self.category_update(id)
        return self.category_add()
