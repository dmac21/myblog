# -*- coding: utf-8 -*-
# @Author  : dmac

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,Column,String,Text,DateTime,Boolean,ForeignKey
from datetime import datetime
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib

pymysql.install_as_MySQLdb()

engine = create_engine('sqlite:///tornado_blog.db',encoding='utf-8',echo=True)
Base = declarative_base(bind=engine)
Session=sessionmaker(bind=engine)
session=Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))
    confirmed = Column(Boolean, default=False)
    name = Column(String(64))
    location = Column(String(64))
    about_me = Column(Text())
    occupation = Column(String(64))
    industry = Column(String(64))
    avatar_hash = Column(String(32))
    posts = relationship('Post',backref='author', lazy='dynamic')
    register_date = Column(DateTime(), default=datetime.utcnow)
    last_seen = Column(DateTime(), default=datetime.utcnow)


    # def __init__(self, **kwargs):
    #     if self.email is not None and self.avatar_hash is None:
    #         self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    def generate_confirmation_token(self, expiration=3600):
        s=Serializer('some hard to guess key',expires_in=expiration)
        return s.dumps({"confirm":self.id}).decode('utf-8')

    def confirm(self,token):
        s = Serializer('some hard to guess key')
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        session.add(self)
        session.commit()
        return True

    def gravatar(self, size=200, default='identicon', ratting='g'):
        url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d{default}&r={ratting}'.format(url=url, hash=hash, size=size, default=default, ratting=ratting)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(
                email=forgery_py.internet.email_address(),
                username=forgery_py.internet.user_name(),
                password=forgery_py.lorem_ipsum.word(),
                confirmed=True,
                name=forgery_py.name.full_name(),
                location=forgery_py.address.city(),
                about_me=forgery_py.lorem_ipsum.sentence(),
                register_date=forgery_py.date.date(True)
            )
            session.add(u)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()



class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    body = Column(Text())
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = session.query(User).count()
        for i in range(count):
            u = session.query(User).offset(randint(0, user_count-1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1,3)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            session.add(p)
            session.commit()

# User.generate_fake()
# Post.generate_fake()
# User.metadata.create_all()
# u = User(username='dmac21',email='386501732@qq.com',password='f825c9e08b')
# s.add(u)
# s.commit()
# s.close()