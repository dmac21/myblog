# -*- coding: utf-8 -*-
# @Author  : dmac

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,Column,String,VARCHAR,ForeignKey
import pymysql
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
    password = Column(String(64))


# User.metadata.create_all()
# u = User(username='dmac21',email='386501732@qq.com',password='f825c9e08b')
# s.add(u)
# s.commit()
# s.close()