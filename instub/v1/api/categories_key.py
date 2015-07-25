# -*- coding: utf-8 -*-
from flask import request, g
from flask_restful import abort

from . import Resource
from instub.models import Category


class CategoriesKey(Resource):

    def get(self, key):
        category = Category.query.filter(Category.key == key).first()
        if not category:
            abort(404, message='category %s not found' % key)
        return category, 200
