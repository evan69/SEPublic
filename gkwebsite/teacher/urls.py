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
    url(r'^upload_question/$', views.upload, name = 'upload_question'),
    url(r'^manage_test/$', views.manage_test, name='manage_test'),
    # teacher 查看志愿者详情
    url(r'^volunteer_info/$', views.volunteer_info),
    # teacher 编辑志愿者详情
    url(r'^volunteer_info_edit/$', views.volunteer_info_edit),
    # teacher 给学生分组
    url(r'^list_group/$', views.distribute_student),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^add_volunteer/$', views.add_volunteer, name='add_volunteer'),
    url(r'^download_xls/file(\w+\.\w*)/$', views.download_xls, name = 'download_xls'),
    url(r'^message/$', views.view_message, name='view_message'),
    url(r'^edit_test/(.*)/$', views.edit_test, name='edit_test'),
    url(r'^checkscoredetail/$', views.checkscoredetail),
    url(r'^checkscore/$', views.checkscore, name='edit_test'),
    url(r'^manage_activity/$',views.manage_activity, name='manage_activity'),
    url(r'^get_all_activity/$',views.get_all_activity, name='get_all_activity'),
    url(r'^delete_activity/$',views.delete_activity, name='delete_activity'),
    url(r'^wechat_push_stack/$', views.wechat_push_stack, name='wechat_push_stack'),
    url(r'^new_message/$',views.new_message, name='new_message'),
]
