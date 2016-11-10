#coding=utf-8

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree as ET
from django.utils.encoding import smart_str, smart_unicode
import hashlib
import urllib
import urllib2
import json
import time
import sys
import requests
reload(sys)
sys.setdefaultencoding('UTF-8')


Token = "zaoshuizaoqi"
Appid = "wxd1c16a4667e24faf"
Appsecret = "efe75bfad99903dff1ba7a783a354e71"
#server_url = "https://gaokao.northeurope.cloudapp.azure.com/"
server_url = "http://59.66.131.171/"
#server_url = "http://59.66.131.87/"
basic_scope = "snsapi_base"

# return the authority url
def authority(type):
    re_dir = ""
    if type == "profile":
        re_dir = server_url + 'student/profile/'
    elif type == "score":
        re_dir = server_url + 'student/score/'
    else:
        re_dir = server_url + 'login/'
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=%s&scope=%s&state=%s#wechat_redirect"%(Appid, re_dir, "code",basic_scope, "1")
    #result = urllib2.urlopen(url)
    return url


def add_authority(ret_url):
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=%s&scope=%s&state=%s#wechat_redirect" % (
    Appid, ret_url, "code", basic_scope, "1")
    return url

# get code
def get_code(request):
    if request.method == 'GET':
        code = request.GET.get('code', None)
        if code == None:
            return (False, code)
        else:
            print code
            return (True, code)
    else:
        return (False, None)

# get the opendid by code returned from get_code
def get_openid_byCode(_code):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=%s" % (Appid, Appsecret,_code, "authorization_code")
    try:
        result = urllib2.urlopen(url)
    except:
        print "open the url failed"
        return (False, None)

    data = json.load(result)
    if data.has_key('openid'):
        openid = data['openid']
        return (True, openid)
    else:
        return (False, None)