# -*- coding: utf-8 -*-

# TODO: datetime support

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###


DefinitionsCategory = {'required': ['name', 'key', 'cover'], 'type': 'object', 'description': 'media category', 'properties': {'cover': {'type': 'string', 'description': 'cover'}, 'name': {'type': 'string', 'description': 'category name'}, 'key': {'type': 'string', 'description': 'category key'}}}
DefinitionsMedia = {'required': ['id', 'worker_id'], 'type': 'object', 'description': 'media', 'properties': {'worker_id': {'type': 'string', 'description': 'worker_id'}, 'standard_resolution': {'type': 'string', 'description': 'standard_resolution'}, 'created_time': {'type': 'string', 'format': 'datetime'}, 'low_resolution': {'type': 'string', 'description': 'low_resolution'}, 'thumbnail': {'type': 'string', 'description': 'thumbnail'}, 'id': {'type': 'string', 'description': 'media id'}}}
DefinitionsError = {'properties': {'message': {'type': 'string'}, 'code': {'type': 'integer', 'format': 'int32'}, 'fields_': {'type': 'string'}}}

validators = {
    ('medias', 'GET'): {'args': {'required': ['category_key'], 'properties': {'category_key': {'type': 'string', 'description': 'category key'}, 'per_page': {'description': 'per page number', 'default': 20, 'required': False, 'type': 'string'}, 'page': {'description': 'page number', 'default': 1, 'required': False, 'type': 'string'}}}},
}

filters = {
    ('categories_key', 'GET'): {200: {'headers': None, 'schema': DefinitionsCategory}},
    ('categories', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsCategory, 'type': 'array'}}},
    ('medias', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsMedia, 'type': 'array'}}},
}

scopes = {
}


class Security(object):

    def __init__(self):
        super(Security, self).__init__()
        self._loader = lambda: []

    @property
    def scopes(self):
        return self._loader()

    def scopes_loader(self, func):
        self._loader = func
        return func

security = Security()


def merge_default(schema, value):
    # TODO: more types support
    type_defaults = {
        'integer': 9573,
        'string': 'something',
        'object': {},
        'array': [],
        'boolean': False
    }

    return normalize(schema, value, type_defaults)[0]


def normalize(schema, data, required_defaults=None):
    
    if required_defaults is None:
        required_defaults = {}
    errors = []

    class DataWrapper(object):

        def __init__(self, data):
            super(DataWrapper, self).__init__()
            self.data = data

        def get(self, key, default=None):
            if isinstance(self.data, dict):
                return self.data.get(key, default)
            if hasattr(self.data, key):
                return getattr(self.data, key)
            else:
                return default

        def has(self, key):
            if isinstance(self.data, dict):
                return key in self.data
            return hasattr(self.data, key)

    def _normalize_dict(schema, data):
        result = {}
        data = DataWrapper(data)
        for key, _schema in schema.get('properties', {}).iteritems():
            # set default
            type_ = _schema.get('type', 'object')
            if ('default' not in _schema
                    and key in schema.get('required', []) 
                    and type_ in required_defaults):
                _schema['default'] = required_defaults[type_]
            # get value
            if data.has(key) or type_ in ('object', 'array'):
                result[key] = _normalize(_schema, data.get(key))
            elif 'default' in _schema:
                result[key] = _schema['default']
            elif key in schema.get('required', []):
                errors.append(dict(name='property_missing',
                                   message='`%s` is required' % key))
        return result

    def _normalize_list(schema, data):
        result = []
        if isinstance(data, (list, tuple)):
            for item in data:
                result.append(_normalize(schema.get('items'), item))
        elif 'default' in schema:
            result = schema['default']
        return result

    def _normalize_default(schema, data):
        return data or schema.get('default')

    def _normalize(schema, data):
        if not schema:
            return None
        funcs = {
            'object': _normalize_dict,
            'array': _normalize_list,
            'default': _normalize_default,
        }
        type_ = schema.get('type', 'object')
        if not type_ in funcs:
            type_ = 'default'

        return funcs[type_](schema, data)

    return _normalize(schema, data), errors

