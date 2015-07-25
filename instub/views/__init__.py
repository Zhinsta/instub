# coding: utf-8

from flask import Blueprint

from instub.views.home import HomeView, Welcome
from instub.views.auth import OAuthCodeView, LoginView, LogoutView

from user import blueprint as user_blueprint
from tags import blueprint as tag_blueprint
from media import blueprint as media_blueprint
from category import blueprint as category_blueprint
from sitemap import blueprint as sitemap_blueprint

__all__ = [user_blueprint, category_blueprint, media_blueprint, sitemap_blueprint, tag_blueprint]

blueprint = Blueprint('views', __name__)

blueprint.add_url_rule('/', view_func=HomeView.as_view(b'home'), endpoint='home')
blueprint.add_url_rule('/instagram/redirect/', view_func=OAuthCodeView.as_view(b'instagram_redirect'), endpoint='instagram_redirect')
blueprint.add_url_rule('/auth/login', view_func=LoginView.as_view(b'login'), endpoint='login')
blueprint.add_url_rule('/auth/logout', view_func=LogoutView.as_view(b'logout'), endpoint='logout')
blueprint.add_url_rule('/welcome', view_func=Welcome.as_view(b'welcome'), endpoint='welcome')
