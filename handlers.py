# -*- coding: utf-8 -*-
# @Author  : dmac

import tornado.web

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class LoginHandler(tornado.web.RequestHandler):

     def get(self):
         self.render('login.html')


class LogoutHandler(tornado.web.RequestHandler):

     def get(self):
         self.render('logout.html')


class RegisterHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('register.html')

class ProfileHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('profile.html')

class ArticleHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('article.html')

class ErrorHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('404.html')