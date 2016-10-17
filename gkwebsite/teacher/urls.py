# coding=utf-8
from django.conf.urls import *
from . import views

urlpatterns = [
		url(r'^student_info_edit/$', views.student_info_edit, name='student_info_edit'),
		url(r'^student_info_edit/formsubmit/$', views.student_info_save, name='student_info'),
		url(r'^student_info/edit/$', views.student_info_edit, name='student_info'),
		url(r'^student_info/$', views.student_info_show, name='student_info'),
		url(r'^logout/$', views.teacher_logout, name='logout'),
		url(r'^search_student/$', views.search_student, name='search_student'),
		url(r'^search_volunteer/$', views.search_volunteer, name='search_volunteer'),
		url(r'^add_student/$', views.add_student, name='add_student'),
		# teacher 查看修改个人信息
		url(r'^profile/$', views.profile),
		url(r'^$', views.dashboard, name='dashboard'),
		url(r'^add_volunteer/$', views.add_volunteer, name='add_volunteer')
]
