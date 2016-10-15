# encoding=utf-8
"""gkwebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin

from login import views as loginViews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^teacher/', include('teacher.urls')),

    #    关联login界面
    #    by byr 161003
    url(r'^login/', loginViews.login),
    #   login表单检查
    #   by byr 161006
    url(r'^logincheck/', loginViews.logincheck),
    #   验证码界面
    url(r'^yzm/(\d+)/(\d+)/$', loginViews.gnrtyzm),


    url(r'^student/', include('student.urls')),
	
	#   关联微信处理
	url(r'^wechat/', include('wechat.urls')),
]
