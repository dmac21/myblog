# -*- coding: utf-8 -*-
# @Author  : dmac

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options
import os.path as op
from handlers import *
from models import Base
from tornado import web

define("port",default=5000,type=int,help="app run in the define port")




setting={
    'template_path':op.join(op.dirname(__file__),'templates'),
    'static_path':op.join(op.dirname(__file__),'static'),
    'debug':True,
    'login_url':'/login',
    #'xsrf_cookies':True,
    'cookie_secret':'f825c9e08b'
}

app=tornado.web.Application(
    handlers=[
        web.URLSpec(r'/',MainHandler, name='index'),
        (r'/login',LoginHandler),
        (r'/logout',LogoutHandler),
        (r'/register',RegisterHandler),
        (r'/confirm/(.*)/(.*)', ConfirmHandler),
        (r'/reconfirm/(.*)', ReconfirmHandler),
        (r'/change-password', ChangePasswordHandler),
        (r'/reset-password', ResetPasswordHandler),
        (r'/change-email', ChangeEmailHandler),
        (r'/user', UserprofileHandler),
        (r'/edit-profile', EditUserprofileHandler),
        (r'/write', WriteHandler),
    ],
    **setting,
)


if __name__ == '__main__':
    Base.metadata.create_all()
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()