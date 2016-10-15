from django.conf.urls import *
from .views import Wechat

urlpatterns = [
    url(r'^$', Wechat),
]