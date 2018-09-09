# -*- coding: utf-8 -*-
# @Author  : dmac

import tornado.web
from models import User,session, Post
from utils.email import send_email
from tornado.template import Loader
import time
from datetime import datetime
import os


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        username = self.get_secure_cookie('username')
        if not username:
            return None
        username = username.decode('utf-8')
        user = session.query(User).filter(User.username == username).first()
        return user

class PostHandler(tornado.web.RequestHandler):

    # @tornado.web.authenticated
    def get(self, postid=None):
        if postid:
            post = session.query(Post).filter(Post.id == postid).first()
            self.render('article.html', post=post)
        else:
            self.render('post.html')

class EditHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, postid):
        post = session.query(Post).filter(Post.id == postid).first()
        self.render('edit_post.html', post=post)

    @tornado.web.authenticated
    def post(self, postid):
        title = self.get_argument('title')
        abstract = self.get_argument('abstract')
        source = self.get_argument('source')
        preview = self.get_argument('preview')
        post = session.query(Post).filter(Post.id == postid).first()
        post.title = title
        post.abstract = abstract
        post.body = source
        post.body_html = preview
        post.timestamp = datetime.utcnow()
        session.commit()

class DeleteHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, postid):
        post = session.query(Post).filter(Post.id == postid).first()
        session.delete(post)
        session.commit()
        self.redirect('/')

class UploadHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        upload_path = os.path.join(os.path.dirname(__file__), 'static/upload')

        file = self.request.files['editormd-image-file']
        if not file:
            res = {
                'success': 0,
                'message': u'图片格式异常'
            }
        else:
            # 返回
            for meta in file:
                filename = meta['filename']
                # filename = datetime.now().strftime('%Y%m%d%H%M%S') + filename
                filepath = os.path.join(upload_path, filename)
                with open(filepath, 'wb') as up:
                    up.write(meta['body'])
                res = {
                    'success': 1,
                    'message': u'图片上传成功',
                    'url': '/static/upload/{}'.format(filename)
                }
        self.write(res)

class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        current_page = int(self.get_argument('page', 1))
        pagesize = 10
        total_page_count = int(session.query(Post).count()/pagesize)
        posts = session.query(Post).order_by(Post.timestamp.desc()).limit(pagesize).offset((current_page-1)*pagesize)
        self.render('index.html', posts=posts, total_page_count=total_page_count, current_page=current_page)

    @tornado.web.authenticated
    def post(self):
        current_user = self.get_current_user()
        source = self.get_argument('source')
        preview = self.get_argument('preview')
        abstract = self.get_argument('abstract')
        title = self.get_argument('title')
        post = Post(body=source, body_html=preview, title=title, abstract=abstract, author=current_user)
        session.add(post)
        session.commit()
        self.redirect('/')

class LoginHandler(BaseHandler):

     def get(self):
         self.render('login.html', message='')

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
             self.render('login.html', message='Invalid username or password!')

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
        self.render('login.html', message='An email has been sent to you email-address!')

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
        self.render('login.html', message='A new email has been sent to you email-address!')

class ChangePasswordHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('change_password.html', message='')

    @tornado.web.authenticated
    def post(self):
        username = self.get_current_user()
        old_password = self.get_argument('old_password')
        password = self.get_argument('password')
        user = session.query(User).filter(User.username == username).first()
        if user.verify_password(old_password):
            user.password = password
            session.add(user)
            session.commit()
            self.render('login.html', message='You has been update your password!')
        else:
            self.render('change_password.html', message='Invalid password!')

class ChangeEmailHandler(BaseHandler):

    def get(self):
        self.render('change_email.html')

class ResetPasswordHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('reset_password.html')

class ErrorHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('404.html')

class UserprofileHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        username = self.get_argument('username')
        user = session.query(User).filter(User.username == username).first()
        self.render('user.html', user=user, message='')

class EditUserprofileHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('editprofile.html')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        user = self.get_current_user()
        user.name = self.get_argument('name')
        user.location = self.get_argument('location')
        user.occupation = self.get_argument('occupation')
        user.industry = self.get_argument('industry')
        user.about_me = self.get_argument('about_me')
        session.add(user)
        session.commit()
        self.render('user.html', user=user, message='you has been update you profile')