# -*- coding: utf-8 -*-

import inspect
import json
import tornado.web
from tornado import gen
import uuid
import logging
logger = logging.getLogger(__name__)


def _get_class_that_defined_method(meth):
    for cls in inspect.getmro(meth.__self__.__class__):
        if meth.__name__ in cls.__dict__: return cls
    return None


class CorsMixin(object):

    CORS_ORIGIN = None
    CORS_HEADERS = None
    CORS_METHODS = None
    CORS_CREDENTIALS = None
    CORS_MAX_AGE = 86400

    def set_default_headers(self):
        if self.CORS_ORIGIN:
            self.set_header("Access-Control-Allow-Origin", self.CORS_ORIGIN)

    @tornado.web.asynchronous
    def options(self, *args, **kwargs):
        if self.CORS_HEADERS:
            self.set_header('Access-Control-Allow-Headers', self.CORS_HEADERS)
        if self.CORS_METHODS:
            self.set_header('Access-Control-Allow-Methods', self.CORS_METHODS)
        else:
            self.set_header('Access-Control-Allow-Methods', self._get_methods())
        if self.CORS_CREDENTIALS != None:
            self.set_header('Access-Control-Allow-Credentials',
                "true" if self.CORS_CREDENTIALS else "false")
        if self.CORS_MAX_AGE:
            self.set_header('Access-Control-Max-Age', self.CORS_MAX_AGE)
        self.set_status(204)
        self.finish()

    def _get_methods(self):
        supported_methods = [method.lower() for method in self.SUPPORTED_METHODS]
        #  ['get', 'put', 'post', 'patch', 'delete', 'options']
        methods = []
        for meth in supported_methods:
            instance_meth = getattr(self, meth)
            if not meth:
                continue
            handler_class = _get_class_that_defined_method(instance_meth)
            if not handler_class is tornado.web.RequestHandler:
                methods.append(meth.upper())

        return ", ".join(methods)


class BaseHandler( CorsMixin, tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def initialize(self, **kwargs):
        super(BaseHandler, self).initialize()
        self.session_id = self.get_cookie("sid")
        if not self.session_id:
            self.set_cookie('sid', uuid.uuid4().hex)

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                         "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    def get_current_user(self):
        uid = self.get_secure_cookie("uid")
      
        return uid

    def get_login_url(self):
        self.require_setting("login_url", "@tornado.web.authenticated")
        return self.application.settings["login_url"]
