# coding: utf-8

from flask import Blueprint

from instub.panel.home import Home
from instub.panel.auth import Login, Logout, AdminEdit
from instub.panel.user import Category, Categories, CategoryEdit

blueprint = Blueprint('panel', __name__, url_prefix='/panel')

blueprint.add_url_rule('/', view_func=Home.as_view(b'index'), endpoint='index')

blueprint.add_url_rule('/login', view_func=Login.as_view(b'login'),
                       endpoint='login', methods=["GET", "POST"])
blueprint.add_url_rule('/logout', view_func=Logout.as_view(b'logout'),
                       endpoint='logout', methods=["GET"])

blueprint.add_url_rule('/admin/add', view_func=AdminEdit.as_view(b'admin_add'),
                       endpoint='admin_add', methods=["GET", "POST"])
blueprint.add_url_rule('/admin/<string:id>/edit',
                       view_func=AdminEdit.as_view(b'admin_edit'),
                       endpoint='admin_edit', methods=["GET", "POST"])

blueprint.add_url_rule('/categories',
                       view_func=Categories.as_view(b'categories'),
                       endpoint='categories', methods=["GET"])
blueprint.add_url_rule('/categories/<string:id>',
                       view_func=Categories.as_view(b'category'),
                       endpoint='category', methods=["GET"])
blueprint.add_url_rule('/categories/add',
                       view_func=CategoryEdit.as_view(b'category_add'),
                       endpoint='category_add', methods=["GET", "POST"])
blueprint.add_url_rule('/categories/<string:id>/edit',
                       view_func=CategoryEdit.as_view(b'category_edit'),
                       endpoint='category_edit', methods=["GET", "POST"])
