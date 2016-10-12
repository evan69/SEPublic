# coding=utf-8
from django.conf.urls import *
from . import views

urlpatterns = [
               url(r'^search_student/$', views.search_student, name='search_student_teacher'),

               # teacher 查看修改个人信息
               url(r'^profile/', views.profile),

                ]
