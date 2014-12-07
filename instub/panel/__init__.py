# coding: utf-8

from flask import Blueprint

from instub.panel.home import Home

blueprint = Blueprint('panel', __name__, url_prefix='/panel')

blueprint.add_url_rule('/', view_func=Home.as_view(b'index'), endpoint='index')
