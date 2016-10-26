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
    vol_student_account_list = getattr(vol.getVolunteerAll(
        vol_account), Volunteer.STUDENT_ACCOUNT_LIST)
    if request.is_ajax() and request.method == 'POST':
        t = []
        for account in vol_student_account_list:
            item = stu.getStudentAll(account)
            stu_dic = stu.getStudentAllDictByAccount(account)
            dic = {'id': stu_dic[Student.ID],
                   'name': stu_dic[Student.REAL_NAME],
                   'gender': stu_dic[Student.SEX]['sexlist'][stu_dic[Student.SEX]['sex']],
                   'source': stu_dic[Student.PROVINCE]['provincelist'][stu_dic[Student.PROVINCE]['province']],
                   'school': stu_dic[Student.SCHOOL],
                   'id_card': stu_dic[Student.ID_NUMBER]}
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
        vol_student_account_list = getattr(vol.getVolunteerAll(
            vol_account), Volunteer.STUDENT_ACCOUNT_LIST)
        for account in vol_student_account_list:
            item = stu.getStudentAll(account)
            stu_dic = stu.getStudentAllDictByAccount(account)
            dic = {'id': stu_dic[Student.ID],
                   'name': stu_dic[Student.REAL_NAME],
                   'gender': stu_dic[Student.SEX]['sexlist'][stu_dic[Student.SEX]['sex']],
                   'source': stu_dic[Student.PROVINCE]['provincelist'][stu_dic[Student.PROVINCE]['province']],
                   'school': stu_dic[Student.SCHOOL],
                   'id_card': stu_dic[Student.ID_NUMBER]}
            # 在名字为查询的名字或者什么没输的情况下才加
            if (dic['name'] == name or name == ''):
                t.append(dic)
        return JsonResponse(t, safe=False)  # must use 'safe=False'
    else:
        return HttpResponse('Access denied.')


def volunteer_logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('/login')


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


def dashboard(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('volunteer/dashboard.html')
    c = {'id': id}
    return HttpResponse(t.render(c))


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

    # 检查这个id是否应该让这个志愿者看到
    vol_id = request.session.get('user_id')
    vol_account = vol.idToAccountVolunteer(vol_id)
    vol_student_account_list = getattr(vol.getVolunteerAll(
        vol_account), Volunteer.STUDENT_ACCOUNT_LIST)
    if (stu.idToAccountStudent(str(id)) not in vol_student_account_list):
        return HttpResponse('Access denied')

    account = stu.idToAccountStudent(str(id))
    student = stu.getStudentAll(account)
    stu_dic = stu.getStudentAllDictByAccount(account)
    dic = {
        Student.ID: stu_dic[Student.ID],
        Student.ACCOUNT: stu_dic[Student.ACCOUNT],
        Student.REAL_NAME: stu_dic[Student.REAL_NAME],
        Student.BIRTH: stu_dic[Student.BIRTH].strftime("%Y-%m-%d"),
        Student.ID_NUMBER: stu_dic[Student.ID_NUMBER],

        # Student.TYPE:
        # stu_dic[Student.NATION]['typelist'][stu_dic[Student.NATION]['type']],
        Student.SEX: stu_dic[Student.SEX]['sexlist'][stu_dic[Student.SEX]['sex']],
        Student.NATION: stu_dic[Student.NATION]['nationlist'][stu_dic[Student.NATION]['nation']],
        Student.SCHOOL: stu_dic[Student.SCHOOL],
        Student.CLASSROOM: stu_dic[Student.CLASSROOM],

        Student.ADDRESS: stu_dic[Student.ADDRESS],
        Student.PHONE: stu_dic[Student.PHONE],
        Student.EMAIL: stu_dic[Student.EMAIL],
        Student.DAD_PHONE: stu_dic[Student.DAD_PHONE],
        Student.MOM_PHONE: stu_dic[Student.MOM_PHONE],

        Student.TUTOR_NAME: stu_dic[Student.TUTOR_NAME],
        Student.TUTOR_PHONE: stu_dic[Student.TUTOR_PHONE],
        Student.PROVINCE: stu_dic[Student.PROVINCE]['provincelist'][stu_dic[Student.PROVINCE]['province']],
        Student.MAJOR: stu_dic[Student.MAJOR],
        Student.TEST_SCORE_LIST: stu_dic[Student.TEST_SCORE_LIST],

        Student.RANK_LIST: stu_dic[Student.RANK_LIST],
        Student.SUM_NUMBER_LIST: stu_dic[Student.SUM_NUMBER_LIST],
        Student.ESTIMATE_SCORE: stu_dic[Student.ESTIMATE_SCORE],
        Student.REAL_SCORE: stu_dic[Student.REAL_SCORE],
        Student.REGISTER_CODE: stu_dic[Student.REGISTER_CODE],
        Student.ADMISSION_STATUS: stu_dic[Student.ADMISSION_STATUS],
        Student.TEACHER_LIST: stu_dic[Student.TEACHER_LIST],
        Student.VOLUNTEER_ACCOUNT_LIST: stu_dic[Student.VOLUNTEER_ACCOUNT_LIST],
        Student.COMMENT: stu_dic[Student.COMMENT],
    }

    tmp_dic = stu_dic[Student.ESTIMATE_SCORE]
    try:
        tmp_dic = eval(tmp_dic)
    except:
        tmp_dic = eval('{}')
    sum_score = 0
    for key in tmp_dic.keys():
        sum_score += tmp_dic[key]['score']
    dic[Student.ESTIMATE_SCORE] = str(sum_score)
    return HttpResponse(t.render({'student': dic}))


def date_choose(request):
    if 'user_id' not in request.session.keys():
        return redirect('/login/')
    t = get_template('volunteer/v_date_choose.html')
    # t = get_template('volunteer/test.html')
    return HttpResponse(t.render({}))


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
        # dict = {
        #     'volunteer_name': getattr(volunteer, Volunteer.REAL_NAME, ' '),
        #     'email': getattr(volunteer, Volunteer.EMAIL, ' '),
        #     'work_address': getattr(volunteer, Volunteer.AREA, ' '),
        #     'home_address': '130',
        #     'postcode': '43',
        #     'homephone': getattr(volunteer, Volunteer.FIXED_PHONE, ' '),
        #     'phone': getattr(volunteer, Volunteer.PHONE, ' '),
        #     'qqn': '85',
        #     'weichat': '66',
        #     'describe': getattr(volunteer, Volunteer.COMMENT, ' '),
        # }

        dict = {'volunteer_name': 'volunteer_name',
                'email': 'email',
                'work_address': 'work_address',
                'home_address': '130',
                'postcode': '43',
                'homephone': '49',
                'phone': 'phone',
                'qqn': '85',
                'weichat': '66',
                'describe': 'describe', }
        return render(request, 'v_userinfo.html', {'dict': dict})
