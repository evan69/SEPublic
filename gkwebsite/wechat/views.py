
# Create your views here.
'''from django.http import HttpResponse
=======
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
>>>>>>> 7d557b336747398e35c5401c77f6c97bf1709038
import hashlib
import urllib

Token = "zaoshuizaoqi"
Appid = "wxd1c16a4667e24faf"
Appsecret = "efe75bfad99903dff1ba7a783a354e71"
token_dic = {}


def wechat_main(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    if request.method == "GET":
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        token = "zaoshuizaoqi"
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
'''
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree as ET
from django.utils.encoding import smart_str, smart_unicode
import hashlib
import urllib
import time

Token = "zaoshuizaoqi"
Appid = "wxd1c16a4667e24faf"
Appsecret = "efe75bfad99903dff1ba7a783a354e71"
token_dic = {}


@csrf_exempt
def wechat_main(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    if request.method == "GET":
        signature = request.GET.get('signature', None)
        # print signature
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        token = "zaoshuizaoqi"
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    elif request.method == "POST":
        print "POST"
        response = HttpResponse(responseMsg(request.body), content_type="application/xml")
        return response


def get_token():
    urls = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
    para = {"appid": Appid, "secret": Appsecret}
    para = urllib.urlencode(para)
    html = urllib.urlopen(urls, para)
    result = html.read()
    print result
    if result.has_key("access_token"):
        token_dic["access_token"] = result["access_token"]
        token_dic["expires_in"] = result["expires_in"]
    else:
        print "access_token fail"
        # get_token()


# 判断ip是否来自于微信
def get_ip():
    urls = "https://api.weixin.qq.com/cgi-bin/getcallbackip"
    para = {"access_token": token_dic["access_token"]}
    para = urllib.urlencode(para)
    html = urllib.urlopen(urls, para)
    result = html.read()
    if result.has_key("ip_list"):
        if result["ip_list"] == ["127.0.0.1", "127.0.0.1"]:
            return True
    return False


def xml2Dic(xmlContent):
    dic = {}
    eT = ET.fromstring(xmlContent)
    if eT.tag == 'xml':
        for child in eT:
            dic[child.tag] = smart_unicode(child.text)
    return dic


def responseMsg(postContent):
    postStr = smart_str(postContent)
    if postStr:
        msg = xml2Dic(postStr)
        print msg
        if msg['MsgType']:
            if msg['MsgType'] == 'event':
                resStr = handleEvent(msg)


def handleEvent(msg):
    if msg['Event'] == 'subscribe':
        resultStr = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', u'感谢关注高考招生辅助系统，目前正在开发中，敬请期待')
    return resultStr

