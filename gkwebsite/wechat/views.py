#coding=utf-8
# Create your views here.
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
        #print "post"
        res_str = responseMsg(request.body)
        print res_str
        response = HttpResponse(res_str, content_type="application/xml")
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
    resStr = "success"
    if postStr:
        msg = xml2Dic(postStr)
        #print msg
        if msg['MsgType']:
            if msg['MsgType'] == 'event':
                resStr = handleEvent(msg)
            elif msg['MsgType'] == 'text':
                resStr = handleText(msg)
    return resStr


def handleEvent(msg):
    resultStr = ""
    if msg['Event'] == 'subscribe':
        # need to add openId in database of opneid openid = msg['FromUserName']
        resultStr = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', u'感谢关注高考招生辅助系统，目前正在开发中，敬请期待')
    elif msg['Event'] == 'unsubscribe':
        # need to delete openid in database of openid, openid = msg['FromUserName]
        resultStr = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', 'sorry...waiting to see you again')
    return resultStr


def handleText(msg):
    resultStr = ""
    if msg['Content'] == u'注册':
        resultStr = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
        login_url = "http://59.66.182.75/login/"
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', login_url)
    return resultStr