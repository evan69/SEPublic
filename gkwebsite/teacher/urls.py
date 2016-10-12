# coding=utf-8
from django.conf.urls import *
import teacher_py.userinfo as userinfo
from . import views

urlpatterns = [
<<<<<<< HEAD
    url(r'^index/', userinfo.index),
		url(r'^search_student/$', views.search_student, name='search_student_teacher'),
        url(r'^student_info_edit/$', views.student_info_edit),
        url(r'^student_info_edit/formsubmit/$', views.student_info_save),
        url(r'^student_info/edit/$', views.student_info_edit),
        url(r'^student_info/$', views.student_info_show),
=======
		url(r'^$', userinfo.index),
>>>>>>> 19d692bd90934eb6f11c61e24aa365d6a8237a5f
		url(r'^fake_backend/$', views.fake_backend),
		url(r'^logout/$', views.teacher_logout),
    url(r'^search_student/$', views.search_student, name='search_student_teacher'),
		url(r'^add_student/$', views.add_student, name='add_student'),
    # teacher 查看修改个人信息
    url(r'^profile/', userinfo.profile), 
		]
