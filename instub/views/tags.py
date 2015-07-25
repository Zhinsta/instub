# coding: utf-8

import gevent

from flask import views, render_template, Blueprint, request

from instagram import InstagramAPI
from instagram import InstagramAPIError

from instub.models import Media
from instub.pager import Pager
from instub.errors import NotFound, InternalServerError
from instub.utils import get_errors, login_required, spawn, open_visit, isfollow

blueprint = Blueprint('tag_view', __name__)


class TagView(views.MethodView):

    @open_visit
    @login_required
    def get(self, name):
        next_url = request.args.get('next_url', None)

        api = InstagramAPI(access_token=request.access_token)
        tag = api.tag(name)
        media = api.tag_recent_media(tag_name=name,
                                     with_next_url=next_url)
        tag = gevent.spawn(api.tag, name)
        media = gevent.spawn(api.tag_recent_media,
                             tag_name=name, with_next_url=next_url)
        gevent.joinall([tag, media])
        try:
            tag, media = tag.get(), media.get()
        except InstagramAPIError:
            return InternalServerError('Internal server error')

        next_url = media[1]
        media = media[0]
        pager = Pager(tag.media_count)
        return render_template('tag.html', tag=tag, pager=pager,
                                media=media, next_url=next_url)


blueprint.add_url_rule('/tags/<string:name>/',
                       view_func=TagView.as_view(b'detail'),
                       endpoint='detail')
