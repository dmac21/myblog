# -*- coding: utf-8 -*-
# @Author  : dmac


class Config(object):

    #调试模式
    DEBUG_MODEL = True
    #默认访问端口
    HTTP_SERVER_PORT = 8000
    #数据库连接地址
    MYSQL_URL = ''
    #邮箱服务器地址
    MAIL_SERVER='smtp.qq.com'
    MAIL_PORT='543'
    MIAL_USER='1073838586@qq.com'
    MIAL_PASS='f825c9e08b'

    pass


config=Config()