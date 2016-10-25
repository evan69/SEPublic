# -*- encoding: utf-8 -*-
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
#Appid = "wxddbda149c7afb981"
#Appsecret = "29473a0ef9f517ae1d1496fc707d0774"
token_dic = {'last_time': 0, 'access_token': ""}


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
        #get_token()
        #createMenu()
        res_str = responseMsg(request.body)
        #print res_str
        response = HttpResponse(res_str, content_type="application/xml")
        return response


def get_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        Appid, Appsecret)
    result = urllib2.urlopen(url).read()
    try:
        token_dic['access_token'] = json.loads(result).get('access_token')
        token_dic['last_time'] = int(time.time())
    except KeyError:
        token_dic['access_token'] = ""
        print "get access_token failed"
    #print token_dic['access_token']


# token() used to update token or use the old token , time limit is 1 hour = 3600s
def token():
    delt = int(time.time()) - token_dic['last_time']
    if delt > 3600:
        get_token()

'''def get_ip():
    urls = "https://api.weixin.qq.com/cgi-bin/getcallbackip"
    para = {"access_token": token_dic["access_token"]}
    para = urllib.urlencode(para)
    html = urllib.urlopen(urls, para)
    result = html.read()
    if result.has_key("ip_list"):
        if result["ip_list"] == ["127.0.0.1", "127.0.0.1"]:
            return True
    return False
'''

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
                createMenu()
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
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', u'感谢关注高考招生辅助系统，回复关键词查看用法\n目前正在开发中，敬请期待')
    elif msg['Event'] == 'unsubscribe':
        # need to delete openid in database of openid, openid = msg['FromUserName]
        resultStr = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', 'sorry...waiting to see you again')
    return resultStr


def handleText(msg):
    # resultStr = ""
    resultStr = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
    if msg['Content'] == u'注册'or msg['Content'] == u'登录':
        # resultStr = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
        login_url = "http://59.66.182.75/login/"
        tmp = u'点击url进入注册/登录界面' + login_url
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', tmp)
    elif msg['Content'] == u'个人信息':
        login_url = "http://59.66.182.75/login/"
        tmp = u'点击url查看个人信息'+ login_url
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', tmp)
    elif msg['Content'] == u'估分':
        login_url = "http://59.66.182.75/login/"
        tmp = u'点击url进入估分系统'+ login_url
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', tmp)
    elif msg['Content'] == u'关键词':
        tmp = u"回复关键词查看相应关键词\n回复注册，进入注册界面\n回复登录，进入登录界面\n回复个人信息，查看个人资料\n回复估分，进入估分系统\n回复更新，查看最新推送"
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', tmp)
    elif msg['Content'] == u'更新':
        resultStr = send_pic_text(msg)
    else:
        tmp = u'TT暂不支持该项功能，回复关键词试试看'
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', tmp)
    return resultStr


def createMenu():
    print 'createMenu'
    token()
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % token_dic['access_token']
    data = '''{
        "button": [
            {
                "name": "基本功能",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "登录",
                        "url": "http://59.66.182.75/login/"
                    },
                    {
                        "type": "view",
                        "name": "注册",
                        "url": "http://59.66.182.75/login/"
                    }]
            },
            {
                "type": "view",
                "name": "估分",
                "url": "http://59.66.182.75/login/"
            },
            {
                "type": "view",
                "name": "个人信息",
                "url": "http://59.66.182.75/login/"

            }
        ]
    }'''
    request = urllib2.urlopen(url, data.encode('utf-8'))

# send text_msg to all users, wechat don't support this function now
'''def send_textMsg(msg):
    print "send_textMsg"
    token()
    url = "https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=%s" % token_dic['access_token']
    data = {
        "filter": {
            "is_to_all": True
        },
        "text": {
            "content": msg
        },
        "msgtype": "text"
    }
    r = requests.post(url=url, data=json.dumps(data, ensure_ascii=False, indent=2))
    result = r.json()
    print result
'''

def send_pic_text(msg):
    newshead = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType>\
    <ArticleCount>%s</ArticleCount><Articles>"
    newsbody = "<item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>"
    newstail = "</Articles></xml>"
    picurl = "http://statics.xiumi.us/xmi/rc/azY5/i/390486cc423f22d66ac517e7267a790b-sz_66475.jpg"
    testurl = "http://r.xiumi.us/board/v3/26Aaa/2801910"
    sendhead = newshead % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'news', '1')
    sendbody = newsbody % (u'五道口的面包房', u'测试图文推送功能', picurl, testurl)
    sendtail = newstail
    resStr = sendhead + sendbody + sendtail
    return resStr