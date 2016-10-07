# encoding=utf-8
from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

import sys
sys.path.append("..")
import database.teacher_backend as teacher_backend


'''
    login & register 界面
    by byr 161003
'''


def login(request):
    return render(request, 'src/login.html')


'''
    login 表单检查
    by byr 161006
'''


@csrf_exempt
def logincheck(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('login_username', ''):
            errors.append('enter login username')
        if not request.POST.get('login_password', ''):
            errors.append('enter login password')
        if not request.POST.get('login_yzm', ''):
            errors.append('enter login yzm')
        if not errors:
            if 'student' in request.POST:
                username = request.POST.get('login_username')
                password = request.POST.get('login_password')
                request.session['user_id'] = 10086
                request.session['user_name'] = username
                request.session['password'] = password
                #return render_to_response('/student')
                return redirect('/student')
            elif 'teacher' in request.POST:
                username = request.POST.get('login_username')
                password = request.POST.get('login_password')
                if teacher_backend.checkPassword(username, password):
                    request.session['user_id'] = 10086
                    request.session['user_name'] = username
                    request.session['password'] = password
                    return HttpResponse(u"教师界面")
                else:
                    return HttpResponse(u"教师界面登录失败")
            elif 'volunteer' in request.POST:
                return HttpResponse(u"志愿者界面")
            else:
                return render_to_response('src/login.html');
    else:
        return render_to_response('src/login.html',
                                  {'errors': errors});
