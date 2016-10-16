
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.wechat_main, name='wechat_main'),
]