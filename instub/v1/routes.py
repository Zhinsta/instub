# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###

from .api.categories_key import CategoriesKey
from .api.categories import Categories
from .api.medias import Medias


routes = [
    dict(resource=CategoriesKey, urls=['/categories/<key>'], endpoint='categories_key'),
    dict(resource=Categories, urls=['/categories'], endpoint='categories'),
    dict(resource=Medias, urls=['/medias'], endpoint='medias'),
]