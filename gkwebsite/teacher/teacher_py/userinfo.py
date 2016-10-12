from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt
from django.template import loader,Context
import copy

import sys
sys.path.append("../../")
import database.teacher_backend as teacher_backend

#from login.login.teacher import userinfo ? for example

keylist = ['account', 'realName', 'password', 'phone', 'email', 'area']
user = {'account': -1, 'realName':"", 'password':"", 'phone': "", 'email': "", 'area':""}
pre = copy.deepcopy(user)

@csrf_exempt
def getFromDatabase():
    global keylist, user, pre
    keylist = ['account', 'realName', 'password', 'phone', 'email', 'area']
    user = {}
    pre = {}
    user['account'] = -1
    for i in range(1,6):
        user[keylist[i]] = teacher_backend.getData(user['account'], keylist[i])
    pre = copy.deepcopy(user)

@csrf_exempt
def index(request):
    #from the login get the user info, and response to the userinfo,html list
    getFromDatabase()
    user['user_id'] = request.session['user_id']
    user['user_name'] = request.session['user_name']
    user['account'] = user['user_name']
    user['password'] = request.session['password']

    if request.method == "GET":
        response = HttpResponse(content_type = "text/html")
        t = loader.get_template("userinfo.html")
        c = Context({"user":user})
        response.write(t.render(c))
        return response
    elif request.method == "POST":
        response = HttpResponse(content_type = "text/html")
        t = loader.get_template("userinfo.html")
        changeDatabase()
        '''user['realName'] = request.POST['realName']
        user['password'] = request.POST['password']
        user['phone'] = request.POST['phone']
        user['email'] = request.POST['email']
        user['area'] = request.POST['area']'''
        c = Context({"user":user})
        response.write(t.render(c))
        return response

@csrf_exempt		
def changeDatabase():
    global user, pre, keylist
    for i in range(1,6):
        if pre[keylist[i]] == request.POST(keylist[i]):
            continue
        else:
            if user[keylist[i]] == request.POST(keylist[i]):
                teacher_backend.setData(user['account'], keylist[i], user[keylist[i]])
