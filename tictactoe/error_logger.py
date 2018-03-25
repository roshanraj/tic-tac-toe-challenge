# -*- coding: utf-8 -*-

from __future__ import absolute_import
from functools import partial
from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient, HTTPError
from raven.base import Client
from raven.contrib.tornado import AsyncSentryClient

DUMMY_EVENT_ID = '00000000000000000000000000000000'


class DummyAsyncSentryClient(Client):
    """A Dummy mixin class that could be used along with request handlers to
    asynchronously send errors to sentry. The client also captures the
    information from the request handlers
    """

    def __init__(self, *args, **kwargs):
        # self.validate_cert = kwargs.pop('validate_cert', True)
        # super(DummyAsyncSentryClient, self).__init__(*args, **kwargs)
        pass

    def is_enabled(self):
        """
        Return a boolean describing whether the client should attempt to send
        events.
        """
        return False

    def capture(self, *args, **kwargs):
        """
        Takes the same arguments as the super function in :py:class:`Client`
        and extracts the keyword argument callback which will be called on
        asynchronous sending of the request

        :return: a 32-length string identifying this event
        """
        if not self.is_enabled():
            return
        return (DUMMY_EVENT_ID,)

    def send(self, auth_header=None, callback=None, **data):
        """
        Serializes the message and passes the payload onto ``send_encoded``.
        """
        pass

    def send_remote(self, url, data, headers=None, callback=None):
        return None

    def _handle_result(self, url, data, future):
        pass

    def _send_remote(self, url, data, headers=None, callback=None):
        """
        Initialise a Tornado AsyncClient and send the reuqest to the sentry
        server. If the callback is a callable, it will be called with the
        response.
        """
        return

