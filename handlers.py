# -*- coding: utf-8 -*-
# @Author  : dmac

import tornado.web
from models import User,s

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')


class MainHandler(BaseHandler):

    #@tornado.web.authenticated
    def get(self):
        self.render('index.html',user=self.current_user)


class LoginHandler(BaseHandler):

     def get(self):
         self.render('login.html',user=self.current_user)

     def post(self):
         username = self.get_argument('username')
         password = self.get_argument('password')
         user=s.query(User).filter(User.username == username).first()
         pw=s.query(User).filter(User.password == password).first()
         if user and pw:
             self.set_secure_cookie('username',username)
             self.redirect('/')
         else:
             self.write('login failed! username :{} , password :{}'.format(username,password))



class LogoutHandler(BaseHandler):

     def get(self):
         self.clear_cookie('username')
         self.redirect('/')


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