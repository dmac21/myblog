# -*- coding: utf-8 -*-
# @Author  : dmac

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def send_email(msg_to,message):
    msg_from='1073838586@qq.com'
    passwd='wkanmnnbqrzchjgb'
    subject='Account confirm'
    msg=MIMEText(message, 'html', 'utf-8')
    msg['Subject']=subject
    msg['From']=formataddr(['Tornado-Blog', msg_from])
    msg['To']= msg_to
    s = smtplib.SMTP_SSL('smtp.qq.com',465)
    try:
        s.login(msg_from,passwd)
        s.sendmail(msg_from,msg_to,msg.as_string())
        print ('发送成功')
    except:
        print ('发送失败')
    finally:
        s.quit()