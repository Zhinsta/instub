# coding: utf-8

import gevent

from flask import views, render_template, Blueprint, request

from instagram import InstagramAPI
from instagram import InstagramAPIError

from instub.models import Media
from instub.errors import NotFound, InternalServerError
from instub.utils import get_errors, login_required, spawn, open_visit, isfollow

blueprint = Blueprint('media_view', __name__)


class MediaView(views.MethodView):

    def _get_meida(self, id, api):
        media = spawn(api.media, id)
        likes = spawn(api.media_likes, media_id=id)
        gevent.joinall([media, likes])
        media, likes = media.get(), likes.get()
        return media, likes

    def _get_errors(self, media, likes):
        errors = get_errors(media, likes)
        if errors:
            if any([e.error_type == 'APINotAllowedError' for e in errors]):
                return render_template('profile-noauth.html', uid=request.uid)
            elif any([e.error_type == 'APINotFoundError' for e in errors]):
                # if image not found delete from database
                media = Media.query.get(id)
                if media:
                    media.delete()
                return NotFound('Media Not Found')
            # app.logger.error([str(e) for e in errors])
            return InternalServerError('Internal Server Error')

    def _get_media_user(self, uid, api):
        try:
            media_user = api.user(uid)
            return media_user
        except InstagramAPIError:
            return None

    @open_visit
    @login_required
    def get(self, id):
        api = InstagramAPI(access_token=request.access_token)
        media, likes = self._get_meida(id, api)
        errors = self._get_errors(media, likes)
        if errors:
            return errors

        uid = media.user.id
        is_follow = False
        if request.uid:
            try:
                is_follow = isfollow(uid, api)
            except InstagramAPIError:
                return InternalServerError('Internal server error')

        media_user = self._get_media_user(uid, api)
        if not media_user:
            return InternalServerError('Internal server error')

        is_star = False
        for i in likes:
            if request.uid and request.uid == i.id:
                is_star = True

        return render_template('media.html', media=media, isfollow=is_follow,
                               media_user=media_user, likes=likes[:5],
                               is_star=is_star)



blueprint.add_url_rule('/media/<id>/',
                       view_func=MediaView.as_view(b'media'),
                       endpoint='media')
