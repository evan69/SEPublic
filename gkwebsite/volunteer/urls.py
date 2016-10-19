# coding=utf-8
from django.conf.urls import *
from . import views

urlpatterns = [
		#url(r'^student_info_edit/$', views.student_info_edit),
		#url(r'^student_info_edit/formsubmit/$', views.student_info_save),
		#url(r'^student_info/edit/$', views.student_info_edit),
        url(r'^student_info/$', views.student_info_show),
		#url(r'^fake_backend/$', views.fake_backend),
		#url(r'^logout/$', views.teacher_logout),
		url(r'^search_student/$', views.search_student, name='search_student_volunteer'),
		url(r'^student_list_all/$', views.student_list_all, name="student_list_all"),
		url(r'^get_volunteer_name_by_id/$',views.get_volunteer_name_by_id, name = "get_volunteer_name_by_id"),
		url(r'^search_student_by_name/$', views.volunteer_search_student_by_name, name="search_student_by_name"),
		#url(r'^add_student/$', views.add_student, name='add_student'),
		# teacher 查看修改个人信息
		url(r'^profile/$', views.profile),
		url(r'^$', views.profile),
]
