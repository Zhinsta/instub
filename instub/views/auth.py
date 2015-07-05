# coding: utf-8

from flask import views
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from instagram import InstagramAPI
from instagram import InstagramAPIError

from instub.models import User
from instub.settings import INSTAGRAM_CLIENT_ID
from instub.settings import INSTAGRAM_CLIENT_SECRET
from instub.settings import INSTAGRAM_REDIRECT_URI
from instub.settings import INSTAGRAM_SCOPE
from instub.errors import NotFound, InternalServerError
from instub.utils import has_login, login_required


class OAuthCodeView(views.MethodView):

    def get(self):
        if has_login():
            return redirect(url_for('views.home'))
        redirect_url = url_for('views.home')
        code = request.args.get('code', '')
        redirect_uri = INSTAGRAM_REDIRECT_URI
        if request.args.get('uri', ''):
            redirect_url = request.args.get('uri')
            redirect_uri += '?uri=' + redirect_url
        api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                           client_secret=INSTAGRAM_CLIENT_SECRET,
                           redirect_uri=redirect_uri)
        try:
            access_token = api.exchange_code_for_access_token(code)
            print access_token
        except:
            return InternalServerError(u'InternalServerError')
        user = (User.query
                .filter_by(id=access_token[1]['id']).first())
        if user:
            user.update(access_token=access_token[0],
                        name=access_token[1]['username'],
                        avatar=access_token[1]['profile_picture'])
        else:
            user = User.create(id=access_token[1]['id'],
                               name=access_token[1]['username'],
                               avatar=access_token[1]['profile_picture'],
                               access_token=access_token[0])
            redirect_url = url_for('views.welcome')
        session.permanent = True
        session['uid'] = user.id
        session['username'] = user.name
        session['access_token'] = user.access_token
        return redirect(redirect_url)


class LoginView(views.MethodView):

    def get(self):
        if has_login():
            return redirect(url_for('views.welcome'))
        redirect_uri = INSTAGRAM_REDIRECT_URI
        if request.args.get('uri', ''):
            redirect_uri += '?uri=' + request.args.get('uri')
        api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                           client_secret=INSTAGRAM_CLIENT_SECRET,
                           redirect_uri=redirect_uri)
        try:
            redirect_uri = api.get_authorize_login_url(scope=INSTAGRAM_SCOPE)
        except InstagramAPIError:
            return InternalServerError(u'Server Error')
        return redirect(redirect_uri)


class LogoutView(views.MethodView):

    @login_required
    def get(self):
        session.pop('uid', None)
        session.pop('username', None)
        session.pop('access_token', None)
        url = url_for('views.home')
        if request.args.get('uri', ''):
            url = request.args.get('uri')
        return redirect(url)

