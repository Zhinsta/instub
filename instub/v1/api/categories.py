# -*- coding: utf-8 -*-

from . import Resource

from instub.models import Category


class Categories(Resource):

    def get(self):
        categories = (Category.query
                      .filter(Category.sort_score > 0)
                      .order_by(Category.sort_score.desc())
                      .all())
        return categories, 200
