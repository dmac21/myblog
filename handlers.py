# -*- coding: utf-8 -*-
# @Author  : dmac

import tornado.web
from models import User,s
from utils.email import send_email


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')


class MainHandler(BaseHandler):

    #@tornado.web.authenticated
    def get(self):
        self.render('index.html',user=self.current_user)

    def put(self):
        self.write('hello dmac')


class LoginHandler(BaseHandler):

     def get(self):
         self.render('login.html',user=self.current_user)

     def post(self):
         username = self.get_argument('username')
         password = self.get_argument('password')
         user=s.query(User).filter(User.username == username).first()
         if user and user.verify_password(password):
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

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = User(username=username, email=email, password=password)
        token = user.generate_confirmation_token()
        s.rollback()
        s.add(user)
        s.commit()
        send_email(msg_to=user.email,confirmurl=token)
        print('An email has been sent to you email-address!')
        self.redirect('/login')


class ErrorHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('404.html')