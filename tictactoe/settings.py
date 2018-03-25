# -*- coding: utf-8 -*-

import logging
import tornado
import tornado.template
import os
import environment
import yaml

from tornado.options import define, options

# Make filepaths relative to settings.
path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")
define("settings", default="config.yaml", help="Settings file for Converse Server")
tornado.options.parse_command_line()

MEDIA_ROOT = path(ROOT, 'media')
TEMPLATE_ROOT = path(ROOT, 'templates')

settings = {}

if options.settings:
    setting_file = options.settings

with open(setting_file, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

settings = cfg

settings['debug'] = options.debug
settings['static_path'] = MEDIA_ROOT
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)

if options.config:
    tornado.options.parse_config_file(options.config)
