# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import url_for, Blueprint
from instub.sitemaps import SitemapView
from instub.database import db

from instub.models import Media

blueprint = Blueprint('site_map', __name__)


class MediaSitemapView(SitemapView):

    def get_objects_count(self):
        return Media.query.count()

    def get_objects(self, offset, limit, **kwargs):
        medias = (db.session.query(
            Media.id,
            Media.worker_id,
            Media.low_resolution,
            Media.thumbnail,
            Media.created_time).
            order_by(Media.created_time.desc()).
            offset(offset).limit(limit))
        return [self.entry_class(
            location=url_for('media_view.media', id=m.id,
                             _external=True, **kwargs),
            lastmod=m.created_time,
            changefreq='daily',
            priority=.9,
            originality=1,
            date_created=m.created_time,
            source=url_for('media_view.media', id=m.id,
                           _external=True, **kwargs),
            category='media page',
            author=m.worker_id
        )for m in medias]


blueprint.add_url_rule(
    '/medias/sitemap.xml', endpoint='media',
    view_func=MediaSitemapView.as_view(b'media_sitemap'))
