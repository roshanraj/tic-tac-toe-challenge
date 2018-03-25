# -*- coding: utf-8 -*-

from tornado.web import url
from tictactoe.handlers.games import GamesHandler, GamesPropertiesHandler
url_patterns = [
    
    # get and post
    url(r'/api/games', GamesHandler),
    # get and post
    url(r'/api/games/(?P<token>[0-9A-Za-z:]+)/$', GamesPropertiesHandler)
]

