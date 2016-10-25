from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.student_center, name='student_center'),
    url(r'^score/$', views.student_score, name='student_score'),
    url(r'^contact/$', views.student_contact, name='student_contact'),
    url(r'^rank/$', views.student_rank, name='student_rank'),
    url(r'^admit/$', views.student_admit, name='student_admit'),
    url(r'^logout/$', views.student_logout, name='student_logout'),
    url(r'^profile/$', views.profile)
]
