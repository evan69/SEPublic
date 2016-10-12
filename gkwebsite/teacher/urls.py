from django.conf.urls import *
import teacher_py.userinfo as userinfo
from . import views

urlpatterns = [
    url(r'^index/', userinfo.index),
		url(r'^search_student/$', views.search_student, name='search_student_teacher'),
    url(r'^student_info_edit/$', views.student_info_edit),
    url(r'^student_info_edit/formsubmit/$', views.student_info_save),
    url(r'^student_info/edit/$', views.student_info_edit),
    url(r'^student_info/$', views.student_info_show),
    ]
