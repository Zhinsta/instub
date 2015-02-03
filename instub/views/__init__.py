# coding: utf-8

from flask import Blueprint

from instub.views.home import HomeView
from instub.views.auth import OAuthCodeView, LoginView, LogoutView

blueprint = Blueprint('views', __name__)

blueprint.add_url_rule('/', view_func=HomeView.as_view(b'home'), endpoint='home')
blueprint.add_url_rule('/instagram/redirect/', view_func=OAuthCodeView.as_view(b'instagram_redirect'), endpoint='instagram_redirect')
blueprint.add_url_rule('/auth/login', view_func=LoginView.as_view(b'login'), endpoint='login')
blueprint.add_url_rule('/auth/logout', view_func=LogoutView.as_view(b'logout'), endpoint='logout')

