# _*_ coding:utf-8 _*_

from django.shortcuts import render
import MySQLdb

from .models import UserMessage


# Create your views here.

def getform(request):
    amessage = None
    all_messages = UserMessage.objects.filter(name="lifantest")
    if all_messages:
        amessage = all_messages[0]

    return render(request, 'message_form.html', {
        "my_message": amessage
    })
