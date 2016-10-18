# encoding=utf-8
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

import sys
sys.path.append("..")
import database.teacher_backend as tch
import database.student_backend as stu
import database.volunteer_backend as vol
import datetime
from database.models import *
from database.my_field import *

# Create your views here.

@ensure_csrf_cookie
def search_student(request):
    if 'user_id' not in request.session.keys():
        return redirect('/login/')
    # for debug here
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('volunteer/v_list_student.html')
    c = {'id': id}
    return HttpResponse(t.render(c))


def student_list_all(request):
    if 'user_id' not in request.session.keys():
        return redirect('/login/')
    vol_id = request.session.get('user_id')
    vol_account = vol.idToAccountVolunteer(vol_id)
    vol_student_account_list = getattr(vol.getVolunteerAll(vol_account), Volunteer.STUDENT_ACCOUNT_LIST)

    if request.is_ajax() and request.method == 'POST':
        t = []
        for account in vol_student_account_list:
            item = stu.getStudentAll(account)
            dic = {'id': getattr(item, 'id'),
                   'name': getattr(item, Student.REAL_NAME),
                   'gender': sexIntToString(getattr(item, Student.SEX)),
                   'source': provinceIntToString(getattr(item, Student.PROVINCE)),
                   'school': getattr(item, Student.SCHOOL),
                   'id_card': getattr(item, Student.ID_NUMBER)}
            t.append(dic)
        return JsonResponse(t, safe=False)  # must use 'safe=False'
    else:
        return HttpResponse('Access denied.')

def volunteer_search_student_by_name(request):
    if 'user_id' not in request.session.keys():
        return redirect('/login/')
    '''
		后端需要在这里改代码，根据姓名搜索学生
		姓名可以通过request.POST.get('name')获取
	'''
    if request.is_ajax() and request.method == 'POST':
        name = request.POST.get('name')
        t = []
        vol_id = request.session.get('user_id')
        vol_account = vol.idToAccountVolunteer(vol_id)
        vol_student_account_list = getattr(vol.getVolunteerAll(vol_account), Volunteer.STUDENT_ACCOUNT_LIST)
        for account in vol_student_account_list:
            item = stu.getStudentAll(account)
            dic = {'id': getattr(item, 'id'),
                   'name': getattr(item, Student.REAL_NAME),
                   'gender': sexIntToString(getattr(item, Student.SEX)),
                   'source': provinceIntToString(getattr(item, Student.PROVINCE)),
                   'school': getattr(item, Student.SCHOOL),
                   'id_card': getattr(item, Student.ID_NUMBER)}
            # 在名字为查询的名字或者什么没输的情况下才加
            if(dic['name'] == name or name == ''):
                t.append(dic)
            else:
                print dic['name'] + " " + name
        # dic = {'id': '100',
        #         'name': '101',
        #         'gender': '102',
        #         'source': '103',
        #         'school': '104',
        #         'id_card': '105'}
        # t.append(dic)
        return JsonResponse(t, safe=False)  # must use 'safe=False'
    else:
        return HttpResponse('Access denied.')

def get_volunteer_name_by_id(request):
    if 'user_id' not in request.session.keys():
        return redirect('/login/')
    # completed by evan69
    # use this if-else to block violent access
    if request.is_ajax() and request.method == 'POST':
        id = request.POST.get('id')
        account = vol.idToAccountVolunteer(id)
        t = {'name': vol.getVolunteer(account, 'realName')}
        return JsonResponse(t)
    else:
        return HttpResponse('Access denied.')

'''
def student_info_show(request):
    if 'user_id' not in request.session.keys():
        return redirect('/login/')
    t = get_template('volunteer/student_info.html')
    c = Context({})
    print request.session.get('user_id')
    return HttpResponse(t.render(c))

'''

@csrf_exempt
def student_info_show(request):
    if 'user_id' not in request.session.keys():
        return redirect('/login/')
    t = get_template('volunteer/student_info.html')
    id = request.GET.get('stu_id', -1)
    if id == -1:
        # 后端需要在这里加上一类条件，即另一种情况下的Access denied
        # 根据request.session.get('user_id')获取志愿者ID，前面代码中的id变量为学生id
        # 要据此排除学生不是该志愿者权限范围内的情况
        return HttpResponse('Access denied')
    account = stu.idToAccountStudent(str(id))
    student = stu.getStudentAll(account)
    dic = {
        Student.ACCOUNT: getattr(student, Student.ACCOUNT, 'no'),
        Student.REAL_NAME: getattr(student, Student.REAL_NAME, 'no'),
        Student.BIRTH: getattr(student, Student.BIRTH).strftime("%Y-%m-%d"),
        Student.ID_NUMBER: getattr(student, Student.ID_NUMBER, 'no'),

        Student.TYPE: getattr(student, Student.TYPE, 'no'),
        Student.SEX: getattr(student, Student.SEX, 'no'),
        Student.NATION: getattr(student, Student.NATION, 'no'),
        Student.SCHOOL: getattr(student, Student.SCHOOL, 'no'),
        Student.CLASSROOM: getattr(student, Student.CLASSROOM, 'no'),

        Student.ADDRESS: getattr(student, Student.ADDRESS, 'no'),
        Student.PHONE: getattr(student, Student.PHONE, 'no'),
        Student.EMAIL: getattr(student, Student.EMAIL, 'no'),
        Student.DAD_PHONE: getattr(student, Student.DAD_PHONE, 'no'),
        Student.MOM_PHONE: getattr(student, Student.MOM_PHONE, 'no'),

        Student.TUTOR_NAME: getattr(student, Student.TUTOR_NAME, 'no'),
        Student.TUTOR_PHONE: getattr(student, Student.TUTOR_PHONE, 'no'),
        Student.PROVINCE: getattr(student, Student.PROVINCE, 'no'),
        Student.MAJOR: getattr(student, Student.MAJOR, 'no'),
        Student.TEST_SCORE_LIST: getattr(student, Student.TEST_SCORE_LIST, 'no'),

        Student.RANK_LIST: getattr(student, Student.RANK_LIST, 'no'),
        Student.SUM_NUMBER_LIST: getattr(student, Student.SUM_NUMBER_LIST, 'no'),
        Student.ESTIMATE_SCORE: getattr(student, Student.ESTIMATE_SCORE, 'no'),
        Student.REAL_SCORE: getattr(student, Student.REAL_SCORE, 'no'),
        Student.REGISTER_CODE: getattr(student, Student.REGISTER_CODE, 'no'),
        Student.ADMISSION_STATUS: getattr(student, Student.ADMISSION_STATUS, 'no'),
        Student.TEACHER_LIST: getattr(student, Student.TEACHER_LIST, 'no'),
        Student.VOLUNTEER_ACCOUNT_LIST: getattr(student, Student.VOLUNTEER_ACCOUNT_LIST, 'no'),
        Student.COMMENT: getattr(student, Student.COMMENT, 'no'),

         }
    print str(dic)
    # return JsonResponse(dic)
    return HttpResponse(t.render({'student':dic}))


@csrf_exempt
def profile(request):
    if 'user_id' not in request.session.keys():
        return redirect('/login/')
    vol_id = request.session.get('user_id')
    print "vol id" + str(vol_id)
    vol_account = vol.idToAccountVolunteer(str(vol_id))
    volunteer = vol.getVolunteerAll(vol_account)
    if request.method == 'POST':
        '''
        	后端需要在这里改代码，保存传进来的数据到数据库，并返回正确的dict。
        	希望能够返回是否保存成功，以及哪些字段不合法的信息
        	后端可以通过request.session.get('user_id')获取id
        '''
        # print request.POST

        volunteer_name = request.POST.get('volunteer_name', 'byr')
        email = request.POST.get('email', 'byr')
        work_address = request.POST.get('work_address', 'byr')
        phone = request.POST.get('phone', '110')
        describe = request.POST.get('describe', 'byr')

        vol.setVolunteer(vol_account, Volunteer.REAL_NAME, volunteer_name)
        vol.setVolunteer(vol_account, Volunteer.EMAIL, email)
        vol.setVolunteer(vol_account, Volunteer.PROVINCE, work_address)
        vol.setVolunteer(vol_account, Volunteer.PHONE, phone)
        vol.setVolunteer(vol_account, Volunteer.COMMENT, describe)



        dict = {'volunteer_name': volunteer_name,
                'email': email,
                'work_address': work_address,
                'home_address': '130',
                'postcode': '43',
                'homephone': '49',
                'phone': phone,
                'qqn': '85',
                'weichat': '66',
                'describe': describe, }
        return JsonResponse(dict)
    else:
        '''
            后端需要在这里改代码，从数据库读取正确的dict，并返回
        '''
        dict = {'volunteer_name': getattr(volunteer, Volunteer.REAL_NAME, 'no'),
                'email': getattr(volunteer, Volunteer.EMAIL, 'no'),
                'work_address': getattr(volunteer, Volunteer.PROVINCE, 'no'),
                'home_address': '130',
                'postcode': '43',
                'homephone': '49',
                'phone': getattr(volunteer, Volunteer.PHONE, 'no'),
                'qqn': '85',
                'weichat': '66',
                'describe': getattr(volunteer, Volunteer.COMMENT, 'no'), }
        return render(request, 'v_userinfo.html', {'dict': dict})
