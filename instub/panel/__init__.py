# coding: utf-8

from flask import Blueprint

from instub.panel.home import Home
from instub.panel.auth import Login, Logout, AddAdmin

blueprint = Blueprint('panel', __name__, url_prefix='/panel')

blueprint.add_url_rule('/', view_func=Home.as_view(b'index'), endpoint='index')
blueprint.add_url_rule('/login', view_func=Login.as_view(b'login'),
                       endpoint='login', methods=["GET", "POST"])
blueprint.add_url_rule('/add_admin', view_func=AddAdmin.as_view(b'add_admin'),
                       endpoint='add_admin', methods=["GET", "POST"])
blueprint.add_url_rule('/logout', view_func=Logout.as_view(b'logout'),
                       endpoint='logout', methods=["GET"])
