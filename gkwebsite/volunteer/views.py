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
import database.backend as back

# Create your views here.


def back_to_profile(request, id):
    vol_account = vol.idToAccountVolunteer(id)
    vol_dic = vol.getVolunteerAllDictByAccount(vol_account)
    volunteer = vol.getVolunteerAll(vol_account)
    dict = {'volunteer_name': vol_dic[Volunteer.REAL_NAME],
            'sex': vol_dic[Volunteer.SEX],
            'email': vol_dic[Volunteer.EMAIL],
            'nation': vol_dic[Volunteer.NATION],
            'province': vol_dic[Volunteer.PROVINCE],
            'department': vol_dic[Volunteer.MAJOR][0],
            'classroom': vol_dic[Volunteer.CLASSROOM],
            'phone': vol_dic[Volunteer.PHONE],
            'qqn': vol_dic[Volunteer.QQ],
            'weichat': vol_dic[Volunteer.WECHAT],
            'distribute': 'no group',
            'describe': vol_dic[Volunteer.COMMENT],
            'password': vol_dic[Volunteer.PASSWORD],
            'studentID': vol_dic[Volunteer.STUDENT_ID], }
    dict['distribute'] = vol.getVolunteerGroupIDListString(volunteer)
    dict['auth'] = "0"  # 后端需要在这里加上权限检查，没权限为0
    # print 'asdfjasdufo9789234759384759________________________'
    return render(request, 'volunteer/v_userinfo.html', {'dict': dict})

def check_identity(identity):
    def decorator(func):
        def wrapper(request, *args, **kw):
            # 下面这空白的位置填session相应的id名
            identity_dic = {'student': 'student_id', 'volunteer': 'volunteer_id', 'teacher': 'teacher_id'}
            id = int(request.session.get(identity_dic[identity]))
            if identity == 'student':
                if stu.is_have_permission(id) == False:
                    pass
            elif identity == 'volunteer':
                if vol.is_have_permission(id) == False:
                    return back_to_profile(request, id)
            else:
                pass
            return func(request, *args, **kw)
        return wrapper
    return decorator


@ensure_csrf_cookie
@check_identity('volunteer')
def search_student(request):
    if 'volunteer_id' not in request.session.keys():
        return redirect('/login/')
    id = request.session.get('volunteer_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('volunteer/v_list_student.html')
    c = {'id': id}
    return HttpResponse(t.render(c))


def student_list_all(request):
    if 'volunteer_id' not in request.session.keys():
        return redirect('/login/')
    vol_id = request.session.get('volunteer_id')
    vol_account = vol.idToAccountVolunteer(vol_id)
    vol_student_id_list = vol.get_can_see_students(vol_id)
    vol_student_account_list = []
    for item in vol_student_id_list:
        vol_student_account_list.append(stu.idToAccountStudent(item))
    print 'sadfasdf', vol_student_account_list
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
    if 'volunteer_id' not in request.session.keys():
        return redirect('/login/')
    '''
        后端需要在这里改代码，根据姓名搜索学生
        姓名可以通过request.POST.get('name')获取
    '''
    if request.is_ajax() and request.method == 'POST':
        name = request.POST.get('name')
        t = []
        vol_id = request.session.get('volunteer_id')
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
        del request.session['volunteer_id']
    except KeyError:
        pass
    return redirect('/login')


def get_volunteer_name_by_id(request):
    if 'volunteer_id' not in request.session.keys():
        return redirect('/login/')
    # completed by evan69
    # use this if-else to block violent access
    # print 'vol_name'
    if request.is_ajax() and request.method == 'POST':
        id = request.POST.get('id')
        account = vol.idToAccountVolunteer(id)
        t = {'name': vol.getVolunteer(account, 'realName')}
        # t = {'name': '李昊阳（调试信息）'}
        return JsonResponse(t)
    else:
        return HttpResponse('Access denied.')


def dashboard(request):
    id = request.session.get('volunteer_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('volunteer/dashboard.html')
    c = {'id': id}
    return HttpResponse(t.render(c))


@csrf_exempt
@check_identity('volunteer')
def student_info_show(request):
    if 'volunteer_id' not in request.session.keys():
        return redirect('/login/')
    t = get_template('volunteer/student_info.html')
    id = request.GET.get('stu_id', -1)
    if id == -1:
        # 后端需要在这里加上一类条件，即另一种情况下的Access denied
        # 根据request.session.get('volunteer_id')获取志愿者ID，前面代码中的id变量为学生id
        # 要据此排除学生不是该志愿者权限范围内的情况
        return HttpResponse('Access denied')

    # 检查这个id是否应该让这个志愿者看到
    vol_id = request.session.get('volunteer_id')
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


@check_identity('volunteer')
def date_choose(request):
    print 'date choose'
    if 'volunteer_id' not in request.session.keys():
        return redirect('/login/')
    id = request.session.get('volunteer_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('volunteer/v_date_choose.html')
    c = {'id': id}
    return HttpResponse(t.render(c))


@csrf_exempt
def get_all_activity(request):
    """
        后端应在此处返回该志愿者可以提交的时间问卷列表，包括填过未填过的
        然后放到下面样例写好的dic的'activity'键对应的列表值中，列表里有若干字典
    """
    print "activity "
    dic = {'activity' : [{'name':'第一次组会','proposer':'李三胖','state':'未填写','activity_id':'12'},
                         {'name':'一对一解答','proposer':'屁孩','state':'已填写','activity_id':'32'},
                         {'name':'庆功会','proposer':'王大神','state':'未填写','activity_id':'9'}]}

    if 'volunteer_id' not in request.session.keys():
        return redirect('/login/')
    id = request.session.get('volunteer_id', -1)
    print 'vol id', id
    ret_list = []
    timer_list = back.getTimerbyDict({})
    for item in timer_list:
        tmp_dic = {}
        info_dic = back.getTimerAllDictByObject(item)
        tmp_dic['name'] = info_dic[Timer.NAME]
        teacher_account = tch.idToAccountTeacher(info_dic[Timer.TEACHER_ID])
        tmp_dic['proposer'] = tch.getTeacher(teacher_account, Teacher.REAL_NAME)
        ret_list.append(tmp_dic)

        vol_dic = info_dic[Timer.VOLUNTEER_DIC]
        if str(id) in vol_dic.keys():
            tmp_dic['state'] = u'已填写'
        else:
            tmp_dic['state'] = u'未填写'
        tmp_dic['activity_id'] = info_dic[Timer.ID]
    dic['activity'] = ret_list
    return JsonResponse(dic)

@csrf_exempt
def get_activity_time(request):
    """
        后端应在此处根据活动的id返回该活动可选择的时间段
        然后放到下面样例写好的dic的'time'键对应的列表值中
        'checked'键表示上次选择的结果
    """
    if 'volunteer_id' not in request.session.keys():
        return redirect('/login/')
    vol_id = str(request.session.get('volunteer_id', -1))
    print 'ac_id=:', request.POST.get('activity_id')
    timer = back.getTimerbyDict({Timer.ID: int(request.POST.get('activity_id'))})[0]
    info_dic = back.getTimerAllDictByObject(timer)
    (time_list, checked_list) = back.date_start_to_end(info_dic[Timer.START_TIME], info_dic[Timer.END_TIME])
    checked_list = []
    for item in time_list:
        checked_list.append('0')
    if vol_id in info_dic[Timer.VOLUNTEER_DIC].keys():
        checked_list = info_dic[Timer.VOLUNTEER_DIC][vol_id]
    dic = {'time': time_list,
           'checked': checked_list}
    return JsonResponse(dic)

@csrf_exempt
def submit_time(request):
    """
        后端应在此处提交本次问卷填写结果
        然后返回是否成功
    """
    if 'volunteer_id' not in request.session.keys():
        return redirect('/login/')
    vol_id = str(request.session.get('volunteer_id'))
    print "vol id" + vol_id
    print request.POST
    ac_id = request.POST.get('activity_id') # 活动问卷的id
    time_list = request.POST.get('time').split(',') # 列表，存储全部可选的时间
    checked_list = request.POST.get('checked').split(',')  # 列表，和上一个列表对应，1表示选中，0表示未选中
    # print ac_id
    # print time_list
    # print checked_list

    timer = back.getTimerbyDict({Timer.ID: int(ac_id)})[0]
    info_dic = back.getTimerAllDictByObject(timer)
    vol_dic = info_dic[Timer.VOLUNTEER_DIC]
    vol_dic[vol_id] = checked_list

    if back.setTimer(timer, Timer.VOLUNTEER_DIC, vol_dic):
        return JsonResponse({'success': 'true'}) # 成功返回true否则false
    else:
        return JsonResponse({'success': 'false'})  # 成功返回true否则false

@csrf_exempt
def profile(request):
    if 'volunteer_id' not in request.session.keys():
        return redirect('/login/')
    vol_id = request.session.get('volunteer_id')
    print "vol id" + str(vol_id)
    vol_account = vol.idToAccountVolunteer(str(vol_id))
    volunteer = vol.getVolunteerAll(vol_account)
    if request.method == 'POST':
        '''
            后端需要在这里改代码，保存传进来的数据到数据库，并返回正确的dict。
            希望能够返回是否保存成功，以及哪些字段不合法的信息
            后端可以通过request.session.get('volunteer_id')获取id
        '''
        volunteer_name = request.POST.get('volunteer_name', 'byr')
        sex = int(request.POST.get('sex', 'byr'))

        email = request.POST.get('email', 'byr')
        nation = int(request.POST.get('nation', 'byr'))
        province = int(request.POST.get('province', 'byr'))

        department = [int(request.POST.get('department', 'byr'))]
        classroom = request.POST.get('classroom', 'byr')

        phone = request.POST.get('phone', '110')
        qqn = request.POST.get('qqn', 'byr')
        weichat = request.POST.get('weichat', 'byr')

        distribute = request.POST.get('distribute', 'byr')
        describe = request.POST.get('describe', 'byr')

        password = request.POST.get('password', 'byr')

        student_id = request.POST.get('studentID', 'byr')

        flag = False

        tmp_stu_list = vol.getVolunteerbyField(Volunteer.STUDENT_ID, student_id)
        if len(tmp_stu_list) == 0 or getattr(tmp_stu_list[0], Volunteer.ACCOUNT) == vol_account:
            vol.setVolunteer(vol_account, Volunteer.STUDENT_ID, student_id)
            vol.setVolunteer(vol_account, Volunteer.REAL_NAME, volunteer_name)
            vol.setVolunteer(vol_account, Volunteer.SEX, sex)
            vol.setVolunteer(vol_account, Volunteer.EMAIL, email)
            vol.setVolunteer(vol_account, Volunteer.NATION, nation)
            vol.setVolunteer(vol_account, Volunteer.PROVINCE, province)
            vol.setVolunteer(vol_account, Volunteer.MAJOR, department)
            vol.setVolunteer(vol_account, Volunteer.CLASSROOM, classroom)
            vol.setVolunteer(vol_account, Volunteer.PHONE, phone)
            vol.setVolunteer(vol_account, Volunteer.QQ, qqn)
            vol.setVolunteer(vol_account, Volunteer.WECHAT, weichat)
            vol.setVolunteer(vol_account, Volunteer.PASSWORD, password)
            if describe.strip() != '':
                describe = vol.getVolunteerAllDictByAccount(vol_account)[Volunteer.COMMENT] + describe + '\n'
            else:
                describe = vol.getVolunteerAllDictByAccount(vol_account)[Volunteer.COMMENT]
            print 'new ', describe
            vol.setVolunteer(vol_account, Volunteer.COMMENT, describe)
            flag = True

        dict = {}
        if flag:
            dict['success'] = 'Y'
        else:
            dict['success'] = 'N'
        dict['message'] = "已更新个人信息" # 后端在此处加message
        return JsonResponse(dict)
    else:
        '''
             后端需要在这里改代码，从数据库读取正确的dict，并返回
        '''
        vol_dic = vol.getVolunteerAllDictByAccount(vol_account)
        dict = {'volunteer_name': vol_dic[Volunteer.REAL_NAME],
                'sex':vol_dic[Volunteer.SEX],
                'email': vol_dic[Volunteer.EMAIL],
                'nation': vol_dic[Volunteer.NATION],
                'province': vol_dic[Volunteer.PROVINCE],
                'department': vol_dic[Volunteer.MAJOR][0],
                'classroom': vol_dic[Volunteer.CLASSROOM],
                'phone': vol_dic[Volunteer.PHONE],
                'qqn': vol_dic[Volunteer.QQ],
                'weichat': vol_dic[Volunteer.WECHAT],
                'distribute': 'no group',
                'describe': vol_dic[Volunteer.COMMENT],
                'password': vol_dic[Volunteer.PASSWORD],
                'studentID': vol_dic[Volunteer.STUDENT_ID],}
        dict['distribute'] = vol.getVolunteerGroupIDListString(volunteer)
        dict['auth'] = "1" # 后端需要在这里加上权限检查，没权限为0
        return render(request, 'volunteer/v_userinfo.html', {'dict': dict})
