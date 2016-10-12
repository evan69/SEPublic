# coding=utf-8
from django.conf.urls import *
from . import views

urlpatterns = [
		url(r'^fake_backend/$', views.fake_backend),
		url(r'^logout/$', views.teacher_logout),
    url(r'^search_student/$', views.search_student, name='search_student_teacher'),
		url(r'^add_student/$', views.add_student, name='add_student'),
    # teacher 查看修改个人信息
    url(r'^profile/', views.profile), 
		]
