# -*- coding: utf-8 -*-
# @Author  : dmac

import tornado.web
from models import User,session
from utils.email import send_email
from tornado.template import Loader
import time


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
         user=session.query(User).filter(User.username == username).first()
         if user and user.verify_password(password):
             if user.confirmed:
                 self.set_secure_cookie('username',username)
                 self.redirect('/')
             else:
                 self.render('unconfirmed.html', username=username)
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
        session.rollback()
        session.add(user)
        session.commit()
        token = user.generate_confirmation_token()
        message = Loader('templates').load('mail_template.html').generate(title="Tornado-blog",username=username,content=token)
        send_email(msg_to=user.email, message=message)
        print('An email has been sent to you email-address!')
        self.redirect('/login')

class ConfirmHandler(BaseHandler):

    def get(self, username, token):
        user = session.query(User).filter(User.username == username).first()
        if user.confirmed:
            self.redirect('/')
        if user.confirm(token):
            self.write('You have been confirmed you account. thanks!')
            time.sleep(2)
            self.set_secure_cookie('username', username)
            self.redirect('/')
        else:
            self.write('The confirmation link is invalid or has expired.')

class ReconfirmHandler(BaseHandler):

    def get(self, username):
        user = session.query(User).filter(User.username == username).first()
        token = user.generate_confirmation_token()
        message = Loader('templates').load('mail_template.html').generate(title="Tornado-blog", username=username, content=token)
        send_email(msg_to=user.email, message=message)
        print('A new email has been sent to you email-address!')
        self.redirect('/login')

class ChangePasswordHandler(BaseHandler):

    def get(self):
        self.render('change_password.html')

class ChangeEmailHandler(BaseHandler):

    def get(self):
        self.render('change_email.html')

class ResetPasswordHandler(BaseHandler):

    def get(self):
        self.render('reset_password.html')

class ErrorHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('404.html')