# -*- coding: utf-8 -*-
# @Author  : dmac

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,Column,String,Text,DateTime
from datetime import datetime
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

pymysql.install_as_MySQLdb()

engine = create_engine('mysql://root:f825c9e08b@127.0.0.1/tornado_blog',encoding='utf-8',echo=True)
Base = declarative_base(bind=engine)
Session=sessionmaker(bind=engine)
s=Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))

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



class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    body = Column(Text)
    posttime = Column(DateTime, index=True, default=datetime.utcnow)

# User.metadata.create_all()
# u = User(username='dmac21',email='386501732@qq.com',password='f825c9e08b')
# s.add(u)
# s.commit()
# s.close()