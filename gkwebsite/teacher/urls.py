# coding=utf-8
from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^fake_backend/$', views.fake_backend),
    url(r'^student_info_edit/$',
        views.student_info_edit,
        name='student_info_edit'),
    url(r'^student_info_edit/formsubmit/$',
        views.student_info_save, name='student_info'),
    url(r'^student_info/edit/$', views.student_info_edit, name='student_info'),
    url(r'^student_info/$', views.student_info_show, name='student_info'),
    url(r'^logout/$', views.teacher_logout, name='logout'),
    url(r'^search_student/$', views.search_student, name='search_student'),
    url(r'^search_volunteer/$', views.search_volunteer, name='search_volunteer'),
    url(r'^add_student/$', views.add_student, name='add_student'),
    # teacher 查看修改个人信息
    url(r'^profile/$', views.profile),
    # teacher 上传试题
    url(r'^release_test/$', views.upload),
    # teacher 查看志愿者详情
    url(r'^volunteer_info/$', views.volunteer_info),
    # teacher 编辑志愿者详情
    url(r'^volunteer_info_edit/$', views.volunteer_info_edit),
    # teacher 给学生分组
    url(r'^list_group/$', views.distribute_student),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^add_volunteer/$', views.add_volunteer, name='add_volunteer'),
    url(r'^download_registration_xls/file(\w+\.\w*)/$', views.download_registration_xls, name = 'download_registration_xls')
]
