# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from math import ceil

from flask import render_template, request


class Pagination(object):

    def __init__(self, page, total_count, per_page):
        self.current_page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def offset(self):
        if self.current_page == 1:
            return 0
        return self.per_page * (self.current_page - 1)

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.current_page > 1

    @property
    def has_next(self):
        return self.current_page < self.pages

    def iter_pages(self, left_edge=1, left_current=2,
                   right_current=3, right_edge=1):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
                    (num > self.current_page - left_current - 1 and
                     num < self.current_page + right_current) or \
                    num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


class Pager(object):

    template = 'pager.html'

    def __init__(self, total_count, per_page=20):
        self.per_page = per_page
        self.limit = per_page
        self.total_count = total_count
        self.url = request.base_url
        self.current_page = int(request.args.get('page', 1))
        self.pagination = Pagination(
            self.current_page, self.total_count, self.per_page)
        self.offset = self.pagination.offset

    def __call__(self):
        pagers = []
        for page in self.pagination.iter_pages():
            url = None
            if page is not None:
                url = '%s?page=%s' % (self.url, page)
            pagers.append({'url': url,
                           'page': page})
        return render_template(self.template, pagers=pagers)
