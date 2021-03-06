# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urlparse import urlparse
from datetime import datetime
from datetime import timedelta

from .app import app


@app.template_filter()
def timestamp(value):
    if not isinstance(value, (int, long, float)):
        value = 0
    return datetime.fromtimestamp(value)


@app.template_filter()
def parseisoformat(value):
    return datetime.parseisoformat(value)


@app.template_filter()
def iproxy(url):
    url = urlparse(url)
    return 'http://instub.com:8000/' + (url.netloc + url.path).encode('base64').strip()


@app.template_filter()
def image(url):
    params = url.split(':')
    media_type = params[0]
    if media_type == 'Image':
        return url[len(media_type) + 2:]


@app.template_filter()
def time_since(dt, default='just now'):
    """将 datetime 替换成字符串 ('3小时前', '2天前' 等等)
    的 Jinja filter copy from
    https://github.com/tonyblundell/socialdump/blob/master/socialdump.py
    """
    if not dt:
        return ''

    now = datetime.now()
    diff = now - dt
    diff = diff - timedelta(seconds=28800)
    total_seconds = int(diff.total_seconds())
    if total_seconds > 0:
        if total_seconds < 315360000:
            periods = (
                (total_seconds / 86400, 'days'),
                (total_seconds / 3600, 'hours'),
                (total_seconds / 60, 'minites'),
                (total_seconds, 'seconds'),
            )
            for period, unit in periods:
                if period > 0:
                    return '%d %s ago' % (period, unit)
            return default
        elif total_seconds < 86400 and dt.day == now.day:
            return 'today ' + dt.strftime('%H:%M')
        else:
            return unicode(dt.strftime('%Y-%m-%d %H:%M'))
    else:
        return default
