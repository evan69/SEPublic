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
    #    关联login界面
    #    by byr 161003
    url(r'^login/', loginViews.login),
    #   login表单检查
    #   by byr 161006
    url(r'^logincheck/', loginViews.logincheck),
    url(r'^student/', include('student.urls')),
]
