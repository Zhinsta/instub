# -*- coding: utf-8 -*-

from flask import render_template
from werkzeug.exceptions import (HTTPException as _HTTPException,
                                 BadRequest as _BadRequest,
                                 Unauthorized as _Unauthorized,
                                 Forbidden as _Forbidden,
                                 NotFound as _NotFound,
                                 InternalServerError as _InternalServerError,
                                 MethodNotAllowed as _MethodNotAllowed)


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        # return render_template("{0}.html".format(error_code)), error_code
        if isinstance(error, _HTTPException):
            message = error.description
        else:
            message = error.message
        if error_code == 401:
            message = u'您需要登录'
        return render_template('errors.html',
                               message=message, error=error), error_code
    for errcode in [401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)
        # app.register_error_handler(errcode, render_error)
    return None


class InstubException(Exception):
    pass


class HTTPException(InstubException, _HTTPException):
    """封装原有方法, 实现自定义模板"""

    def get_body(self, environ):
        """Get the HTML body."""
        return render_template('errors.html', error=self)


class BadRequest(HTTPException, _BadRequest):
    pass


class Unauthorized(HTTPException, _Unauthorized):
    pass


class Forbidden(HTTPException, _Forbidden):
    pass


class NotFound(HTTPException, _NotFound):
    pass


class InternalServerError(HTTPException, _InternalServerError):
    pass


class MethodNotAllowed(HTTPException, _MethodNotAllowed):
    pass
