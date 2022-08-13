# _*_ encoding:utf-8 _*_
from random import Random

from users.models import EmailVerifyRecord
from LfLearning.settings import EMAIL_FROM
from django.core.mail import send_mail

__author__ = 'lifan'
__date__ = '2017/3/2 下午1:12'


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    random_code = random_str(16)
    email_record.code = random_code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "LF-Learning注册激活链接"
        email_body = "请使用该链接来激活账号: http://127.0.0.1:8000/active/{0}".format(random_code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "LF-Learning密码重置"
        email_body = "请使用该链接来重置您的密码: http://127.0.0.1:8000/reset/{0}".format(random_code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
