# coding:utf-8
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
import hashlib

# Create your views here.

class Wechat(View):
    # token = "zaoshuizaoqi"
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(self, Wechat).dispatch(*args, **kwargs)

    # check the signature and try to connect the server
    def get(self, request):
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        token = "zaoshuizaoqi"
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join(hashlist)
        hashstr = hashlib.sha1(hashstr).hexdigest()
        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("Wechat index")
