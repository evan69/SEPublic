# coding=utf-8
from django.conf.urls import *
import teacher_py.userinfo as userinfo
from . import views

urlpatterns = [url(r'^$', userinfo.index),
               url(r'^search_student/$', views.search_student, name='search_student_teacher'),

               # teacher 查看修改个人信息
               url(r'^profile/', userinfo.profile), ]
