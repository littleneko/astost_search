#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


import tornado.ioloop
import tornado.web

from tornado.options import define, options

from main_handler import MainHandler
from result_handler import ResultHandler
from item_module import ItemModule
from login_handle import LoginHandler
from reg_handle import RegisterHandler


define("port", default=8000, help="run on the given port", type=int)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/s', ResultHandler),
        (r'/login', LoginHandler),
        (r'/reg', RegisterHandler)
    ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        ui_modules={'Item': ItemModule})

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()