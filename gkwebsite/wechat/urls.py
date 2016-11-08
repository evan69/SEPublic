
from django.conf.urls import url
from . import views, wechat_api

urlpatterns = [
    url(r'^$', views.wechat_main, name='wechat_main'),
    url(r'^auth/$', wechat_api.authority, name="authority")
]
