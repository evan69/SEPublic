from django.conf.urls import *
import teacher_py.userinfo as userinfo
from . import views

urlpatterns = [
    url(r'^index/', userinfo.index),
		url(r'^search_student/$', views.search_student, name='search_student_teacher'),
		url(r'^fake_backend/$', views.fake_backend),
		url(r'^logout/$', views.teacher_logout),
		url(r'^add_student/$', views.add_student, name='add_student'),
    ]
