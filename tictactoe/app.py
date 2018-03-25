#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tic-tac-toe
======
Tic-tac-toe is a gaming api.
------------------
The Tic-tac-toe package, at its core, is a Tornado based server. 

"""

import os
import logging
import socket
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options
from tornado import gen
# import momoko
from tictactoe.settings import settings
from tictactoe.urls import url_patterns


enable_uvloop = False
is_windows = os.name == 'nt'


class App(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)
        

def main():
    app = App()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    if settings.get('debug', False) and not is_windows:
        tornado.ioloop.IOLoop.instance().set_blocking_log_threshold(0.1)
    tornado.ioloop.IOLoop.instance().start()
  
def print_banner():
    """
    Print ASCII Banner
    :return:
    """
    banner_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banner.txt")
    if os.path.isfile(banner_file):
        with open(banner_file, "r") as bf:
            print(bf.read())


def server():
    print_banner()
    print("Running on port: %s" % options.port)

    if enable_uvloop:
        try:
            from tornaduv import UVLoop

            print("UVLoop set as tornado IOLoop")
            tornado.ioloop.IOLoop.configure(UVLoop)
        except ImportError as ex:
            print("[Warn] LibUV wrapper not available. Check and install libuv-dev, pyuv, tornaduv")
    try:
        main()
    except KeyboardInterrupt as ex:
        print("\nInstance shut down...")
        print("")


if __name__ == "__main__":
    server()
