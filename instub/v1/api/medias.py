# -*- coding: utf-8 -*-
from flask import request, g
from flask_restful import abort

from . import Resource
from instub.models import Category


class Medias(Resource):

    def get(self):
        key = g.args.get('category_key')
        page = int(g.args.get('page'))
        per_page = int(g.args.get('per_page'))
        category = Category.query.filter(Category.key == key).first()
        if not category:
            abort(404, message='category %s not found' % key)
        offset = per_page * (page - 1)
        medias = category.medias(category.id, limit=per_page, offset=offset)

        return medias, 200
