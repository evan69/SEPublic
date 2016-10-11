from django.conf.urls import *
import teacher_py.userinfo as userinfo
from . import views

urlpatterns = [
    url(r'^index/', userinfo.index),
		url(r'^search_student/$', views.search_student, name='search_student_teacher'),
    ]
