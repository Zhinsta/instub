# -*- coding: utf-8 -*-

import gevent
from gevent.util import wrap_errors

import itsdangerous
from flask import views
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import Blueprint
from flask import render_template
from instagram import InstagramAPI
from instagram import InstagramAPIError

from instub.errors import InternalServerError
from instub.utils import has_login, login_required

signer = itsdangerous.URLSafeSerializer('fbxrinima')

blueprint = Blueprint('user_view', __name__)


class ProfileView(views.MethodView):

    @login_required
    def get(self, uid=None):
        next_url = request.args.get('next_url', None)
        if next_url and 'instagram' not in next_url:
            next_url = signer.loads(next_url)
        api = InstagramAPI(access_token=request.access_token)

        user = gevent.spawn(wrap_errors(InstagramAPIError, api.user),
                            user_id=uid)
        feeds = gevent.spawn(wrap_errors(InstagramAPIError,
                             api.user_recent_media),
                             user_id=uid, with_next_url=next_url)
        if request.uid:
            isfollows = spawn(isfollow, uid, api)
        else:
            isfollows = spawn(lambda x: False, uid)

        gevent.joinall([user, feeds, isfollows])
        user, feeds, isfollows = user.get(), feeds.get(), isfollows.get()
        errors = [e for e in (user, feeds, isfollows)
                  if isinstance(e, InstagramAPIError)]
        if errors:
            if any([e.error_type == 'APINotAllowedError' for e in errors]):
                return render('profile-noauth.html', uid=uid)
            if any([e.error_type == 'APINotFoundError' for e in errors]):
                return notfound(u'用户不存在')
            app.logger.error([str(e) for e in errors])
            return InternalServerError('Internal Server Error')

        next_url = feeds[1] if feeds else None
        next_url = signer.dumps(next_url) if next_url else next_url
        feeds = feeds[0] if feeds else []
        isme = False
        if request.uid and uid == request.uid:
            isme = True
        return render_template(
            'profile.html',
            user=user,
            feeds=feeds,
            isme=isme,
            isfollow=isfollows,
            next_url=next_url)


blueprint.add_url_rule('/profile/<uid>/',
                       view_func=ProfileView.as_view(b'profile'),
                       endpoint='profile')


class FollowBaseView(object):

    def _get_users(self, uid, user_type='followed'):
        next_url = request.args.get('next_url', None)
        if next_url and 'instagram' not in next_url:
            next_url = signer.loads(next_url)
        api = InstagramAPI(access_token=request.access_token)
        user = spawn(api.user, uid)
        if user_type == 'following':
            users = spawn(api.user_follows, uid, with_next_url=next_url)
        else:
            users = spawn(api.user_followed_by, uid, with_next_url=next_url)
        isfollows = False
        if request.uid:
            isfollows = spawn(isfollow, uid, api)
        else:
            isfollows = spawn(lambda x: False, uid)

        gevent.joinall([user, users, isfollows])
        user, users, isfollows = user.get(), users.get(), isfollows.get()
        errors = get_errors(user, users, isfollows)
        if errors:
            app.logger.error([str(e) for e in errors])
            return notfound(u'服务器暂时出问题了')

        next_url = users[1]
        next_url = signer.dumps(next_url) if next_url else next_url
        users = users[0]

        isme = False
        if request.uid and uid == request.uid:
            isme = True
        context = {
            'user': user,
            'users': users,
            'next_url': next_url,
            'isfollows': isfollows,
            'isme': isme,
        }
        return context


class FollowerView(views.MethodView, FollowBaseView):

    @login_required
    def get(self, uid):
        context = self._get_users(uid)
        if isinstance(context, tuple):
            return context
        context['message'] = u'关注者'
        return render_template('follower.html', **context)


class FollowingView(views.MethodView, FollowBaseView):

    @login_required
    def get(self, uid):
        context = self._get_users(uid, user_type='following')
        if isinstance(context, tuple):
            return context
        context['message'] = u'关注中'
        return render_template('follower.html', **context)


blueprint.add_url_rule('/follower/<uid>/',
                       view_func=FollowerView.as_view(b'follower'),
                       endpoint='follower')
blueprint.add_url_rule('/following/<uid>/',
                       view_func=FollowingView.as_view(b'following'),
                       endpoint='following')
