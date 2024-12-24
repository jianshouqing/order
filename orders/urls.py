from django.contrib import admin
from django.urls import path
from app01.views import account
urlpatterns = [
    path("login/", account.login, name='login'),
    path("sms/login/", account.sms_login, name='sms_login'),
    path("send/sms/", account.send_sms, name='send_sms'),
    path("home/", account.home, name='home'),
]
