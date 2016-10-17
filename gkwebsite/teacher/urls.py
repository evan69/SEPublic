# coding=utf-8
from django.conf.urls import *
from . import views

urlpatterns = [
		url(r'^student_info_edit/$', views.student_info_edit),
		url(r'^student_info_edit/formsubmit/$', views.student_info_save),
		url(r'^student_info/edit/$', views.student_info_edit),
		url(r'^student_info/$', views.student_info_show),
		url(r'^fake_backend/$', views.fake_backend),
		url(r'^logout/$', views.teacher_logout),
		url(r'^search_student/$', views.search_student, name='search_student_teacher'),
		url(r'^add_student/$', views.add_student, name='add_student'),
		# teacher 查看修改个人信息
		url(r'^profile/$', views.profile),
		url(r'^$', views.profile),
		# teacher 上传试题
		url(r'^release_test/$', views.upload),
		# teacher 查看志愿者详情
		url(r'^volunteer_info/$', views.volunteer_info),
		# techar 编辑志愿者详情
		url(r'^volunteer_info_edit/$', views.volunteer_info_edit)

]
