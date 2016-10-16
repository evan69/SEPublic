
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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


def get_token():
    urls = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
    para = {"appid":Appid, "secret":Appsecret}
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