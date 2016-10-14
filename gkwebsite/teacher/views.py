#encoding=utf-8
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import  csrf_exempt

import sys
sys.path.append("..")
import database.teacher_backend as tch
from database.models import *


@ensure_csrf_cookie
def search_student(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('teacher/list_student.html')
    c = {'id': id}
    return HttpResponse(t.render(c))

def student_info_edit(request):
    t = get_template('teacher/student_info_edit.html')
    c = Context({})
    return  HttpResponse(t.render(c))


def student_info_save(request):
    t = get_template('teacher/student_info.html')
    c = Context({})
    return HttpResponse(t.render(c))

def student_info_show(request):
    t = get_template('teacher/student_info.html')
    c = Context({})
    return HttpResponse(t.render(c))

def add_student(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    #t = get_template('teacher/list_student.html')
    #c = {}
    #return HttpResponse(t.render(c))
    return HttpResponse('Add student page.')

def fake_backend(request):
    if request.is_ajax() and request.method == 'POST':
        c = {'name':'Alice', 'gender':'男', 'source':'北京', 'school':'人大附中', 'id_card':'11010819980824181X'}
        c['name']=request.POST.get('name')
        t = []
        t.append(c)
        return JsonResponse(t, safe=False)
    else:
        return HttpResponse('Access denied.')

def teacher_logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('/login')

'''
    查看和修改教师个人信息
    by byr 161012
'''
#@csrf_protect
@csrf_exempt
def profile(request):
    if request.method == 'POST':
        '''
            后端需要在这里改代码，保存传进来的数据到数据库，并返回正确的dict
        '''
        teacher_name = request.POST.get('teacher_name', 'byr')
        phone = request.POST.get('phone', '110')
        email = request.POST.get('email', '110')
        work_address = request.POST.get('work_address', '110')
        home_address = request.POST.get('home_address', '110')
        postcode = request.POST.get('postcode', '110')
        homephone = request.POST.get('homephone', '110')
        qqn = request.POST.get('qqn', '110')
        weichat = request.POST.get('weichat', '110')
        describe = request.POST.get('describe', '110')

        id = (int)(request.session.get('user_id'))
        account = tch.idToAccountTeacher(id)

        tch.setTeacher(account, Teacher.REAL_NAME, teacher_name)
        tch.setTeacher(account, Teacher.PHONE, phone)
        tch.setTeacher(account, Teacher.EMAIL, email)
        tch.setTeacher(account, Teacher.AREA, work_address)
        # tch.setTeacher(account, Teacher.AREA, home_address)
        # tch.setTeacher(account, Teacher.REAL_NAME, postcode)
        # tch.setTeacher(account, Teacher.REAL_NAME, homephone)
        # tch.setTeacher(account, Teacher.REAL_NAME, qqn)
        # tch.setTeacher(account, Teacher.REAL_NAME, weichat)
        # tch.setTeacher(account, Teacher.REAL_NAME, describe)

        dict = {'teacher_name': teacher_name,
                'email': email,
                'work_address': work_address,
                'home_address': '10',
                'postcode': '3',
                'homephone': '4',
                'phone': phone,
                'qqn': '5',
                'weichat': '6',
                'describe': '7', }
        return JsonResponse(dict)
    else:
        '''
            后端需要在这里改代码，从数据库读取正确的dict，并返回
        '''
        id = (int)(request.session.get('user_id'))
        account = tch.idToAccountTeacher(id)
        # print 'account ' + account
        teacher = tch.getTeacherAll(account)
        # print 'name' + getattr(teacher, 'realName')
        dict = {
			'teacher_name': getattr(teacher, Teacher.REAL_NAME,'no such attr. by lihy'),
			'email': getattr(teacher, Teacher.EMAIL,'no such attr. by lihy'),
			'work_address': getattr(teacher, Teacher.AREA,'no such attr. by lihy'),
			'home_address': '130',
			'postcode': '43',
			'homephone': '120',
			'phone': getattr(teacher, Teacher.PHONE,'no such attr. by lihy'),
			'qqn': '85',
			'weichat': '66',
			'describe': '57',
		}
        # dict = {'teacher_name': '骚猴', 'email': '11', 'work_address': '22', 'home_address': '130', 'postcode': '43',
        #         'homephone': '49', 'phone': '666', 'qqn': '85', 'weichat': '66', 'describe': '57', }
        return render(request, 'userinfo.html',{'dict':dict})


