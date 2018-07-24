# -*- coding: utf-8 -*-
# @Author  : dmac

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options
import os.path as op
from handlers import *

define("port",default=5000,type=int,help="app run in the define port")




setting={
    'template_path':op.join(op.dirname(__file__),'templates'),
    'static_path':op.join(op.dirname(__file__),'static'),
    'debug':True,
    #'login_url':'/login',
    #'xsrf_cookies':True,
    'cookie_secret':'f825c9e08b'
}

app=tornado.web.Application(
    handlers=[
        (r'/',MainHandler),
        (r'/login',LoginHandler),
        (r'/logout',LogoutHandler),
        (r'/profile/(\w+)',ProfileHandler),
        (r'/article/(\w+)',ArticleHandler),
        (r'/register',RegisterHandler),
    ],
    **setting,
)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()