# coding: utf-8

import gevent

from flask import views
from flask import render_template

from instagram import InstagramAPI
from instagram import InstagramAPIError

from instub.models import User
from instub.utils import get_errors


class MediaView(views.MethodView):

    def get(self, mid):
        api = InstagramAPI(access_token=request.access_token)
        media = spawn(api.media, mid)
        likes = spawn(api.media_likes, media_id=mid)
        gevent.joinall([media, likes])
        media, likes = media.get(), likes.get()
        errors = get_errors(media, likes)
        if errors:
            if any([e.error_type == 'APINotAllowedError' for e in errors]):
                return render('profile-noauth.html', uid=request.uid)
            app.logger.error([str(e) for e in errors])
            return notfound(u'服务器暂时出问题了')

        uid = media.user.id
        isfollows = False
        if request.uid:
            try:
                isfollows = isfollow(uid, api)
            except InstagramAPIError:
                return notfound(u'服务器暂时出问题了')

        isstar = False
        for i in likes:
            if request.uid and request.uid == i.id:
                isstar = True

        isme = False
        if request.uid and uid == request.uid:
            isme = True
        return render('media.html', media=media, isme=isme,
                      isfollow=isfollows, likes=likes[:5], isstar=isstar)
