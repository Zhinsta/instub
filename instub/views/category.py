# coding: utf-8

from flask import views
from flask import Blueprint
from flask import render_template

from instub.errors import NotFound
from instub.models import Category
from instub.pager import Pager

blueprint = Blueprint('category_view', __name__)


class CategoryView(views.MethodView):

    def get(self, name):
        category = Category.query.filter(Category.name == name).first()
        if not category:
            return NotFound('Category Not Found')
        pager = Pager(category.medias_count(category.id))
        medias = category.medias(category.id, limit=pager.per_page,
                                 offset=pager.offset)
        return render_template('medias_list.html', pager=pager,
                               medias=medias, category=category)


blueprint.add_url_rule('/category/<name>/',
                       view_func=CategoryView.as_view(b'category'),
                       endpoint='category')
