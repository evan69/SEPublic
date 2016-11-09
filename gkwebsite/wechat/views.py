#coding=utf-8

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree as ET
from django.utils.encoding import smart_str, smart_unicode
import hashlib
import wechat_api as we
import urllib
import urllib2
import json
import time
import sys
import requests

#from gkwebsite.database.models import WechatURL

reload(sys)
sys.setdefaultencoding('UTF-8')

sys.path.append("../")
import database.backend as back
from database.models import *


Token = "zaoshuizaoqi"
Appid = "wxd1c16a4667e24faf"
Appsecret = "efe75bfad99903dff1ba7a783a354e71"
token_dic = {'last_time': 0, 'access_token': ""}
#server_url = "http://gaokao.northeurope.cloudapp.azure.com/"
#server_url = "http://59.66.182.75/"
server_url = 'http://59.66.131.87/'


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
        #login_url = "http://59.66.131.171/login/"
        '''login_url = we.authority("login")
        login_url = we.authority("login")
        tmp = u'点击url进入注册/登录界面' + login_url
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', tmp)'''
        resultStr = send_pic_text(msg, "login")
    elif msg['Content'] == u'个人信息':
        #login_url = "http://59.66.131.171/login/"
        '''login_url = we.authority("profile")
        login_url = we.authority("profile")
        tmp = u'点击url查看个人信息'+ login_url
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', tmp)'''
        resultStr = send_pic_text(msg, "profile")
    elif msg['Content'] == u'估分':
        #login_url = "http://59.66.131.171/login/"
        '''login_url = we.authority("score")
        login_url = we.authority("score")
        tmp = u'点击url进入估分系统'+ login_url
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', tmp)'''
        resultStr = send_pic_text(msg, "score")
    elif msg['Content'] == u'关键词':
        tmp = u"回复关键词查看相应关键词\n回复注册，进入注册界面\n回复登录，进入登录界面\n回复个人信息，查看个人资料\n回复估分，进入估分系统\n回复更新，查看最新推送"
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', tmp)
    elif msg['Content'] == u'更新':
        resultStr = send_pic_text(msg, "update")
    elif msg['Content'] == u'历史消息':
        resultStr = send_pic_text_many(msg)
    else:
        tmp = u'TT暂不支持该项功能，回复关键词试试看'
        resultStr = resultStr % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', tmp)
    return resultStr


def createMenu():
    print 'createMenu'
    token()
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % token_dic['access_token']

    data = {
        "button": [
            {
                "name": "基本功能",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "登录",

                        "url": we.authority("login")

                    },
                    {
                        "type": "view",

                        "name": "注册",

                        "url": we.authority("login")

                    }]
            },
            {
                "type": "view",

                "name": "估分",

                "url": we.authority("score")

            },
            {
                "type": "view",

                "name": "个人信息",

                "url": we.authority("profile")


            }
        ]

    }
    #request = urllib2.urlopen(url, data.encode('utf-8'))
    #print data
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response = urllib2.urlopen(req, json.dumps(data, ensure_ascii=False))
    result = response.read()
    return HttpResponse(result)



def send_pic_text(msg,type):
    newshead = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType>\
    <ArticleCount>%s</ArticleCount><Articles>"
    newsbody = "<item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>"
    newstail = "</Articles></xml>"
    index_pic = ""
    title = ""
    abstract = ""
    picurl = ""
    texturl = ""
    if type == "update":
        content = back.getLastOneWechatURL()
        if content == None:
            pass
        else:
            title = content[WechatURL.TITLE]
            abstract = content[WechatURL.TEXT]
            picurl = content[WechatURL.PICTURE_URL]
            texturl = content[WechatURL.MESSAGE_URL]
    elif type == "login":
        picurl = index_pic
        title = u'点击进入注册或登录界面'
        texturl = we.authority("login")
    elif type == "profile":
        picurl = index_pic
        title = u'点击查看个人信息'
        texturl = we.authority("profile")
    elif type == "score" :
        picurl = index_pic
        title = u'点击进入估分'
        texturl = we.authority("score")
    #testurl = "http://r.xiumi.us/board/v3/26Aaa/2801910"
    sendhead = newshead % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'news', '1')
    sendbody = newsbody % (title, abstract, picurl, texturl)
    sendtail = newstail
    resStr = sendhead + sendbody + sendtail
    return resStr


def send_pic_text_many(msg):
    newshead = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType>\
       <ArticleCount>%s</ArticleCount><Articles>"
    newsbody = "<item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>"
    newstail = "</Articles></xml>"
    all_content = back.getLastTenWechatURL()
    num = len(all_content)
    sendhead = newshead % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'news', str(num))
    if len == 0:
        title = u'无消息'
        abstract = ""
        picurl = ""
        texturl = ""
        sendbody = newsbody % (title, abstract, picurl, texturl)
        resStr = sendhead + sendbody + newstail
        return resStr
    else:
        sendbody = ""
        for content in all_content:
            title = content[WechatURL.TITLE]
            abstract = content[WechatURL.TEXT]
            picurl = content[WechatURL.PICTURE_URL]
            texturl = content[WechatURL.MESSAGE_URL]
            sendbody = sendbody + newsbody % (title, abstract, picurl, texturl)
        resStr = sendhead + sendbody + newstail
        return resStr

