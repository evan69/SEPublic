# encoding=utf-8
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.template.loader import get_template
from django.template import Context

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

import os
import database.teacher_backend as tch
import database.student_backend as stu
import database.volunteer_backend as vol
import database.image_backend as pic
import database.backend as back
import django.forms as forms
import datetime
from database.models import *
from database.my_field import *


@ensure_csrf_cookie
def search_student(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('teacher/list_student.html')
    c = {'id': id, 'n_item': 15}
    return HttpResponse(t.render(c))


@ensure_csrf_cookie
def manage_activity(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('teacher/manage_activity.html')
    c = {'id': id, 'n_item': 15}
    return HttpResponse(t.render(c))


@ensure_csrf_cookie
def get_all_activity(request):
    '''
        后端在此处返回老师可见的活动列表，放在dic字典的'acticity'键对应的值里
    '''
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    dic = {'activity' : [{'name':'第一次组会','proposer':'李三胖','start_time':'2016/10/1','end_time':'2016/10/10','number':'12','activity_id':'12'},
                         {'name':'一对一解答','proposer':'屁孩','start_time':'2016/10/10','end_time':'2016/10/11','number':'99','activity_id':'32'},
                         {'name':'庆功会','proposer':'王大神','start_time':'2016/10/10','end_time':'2016/10/19','number':'3','activity_id':'9'}]}
    return JsonResponse(dic)


@ensure_csrf_cookie
def search_volunteer(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('teacher/list_volunteer.html')
    c = {'id': id}
    return HttpResponse(t.render(c))


@csrf_exempt
def student_info_edit(request):
    if request.method == 'POST':
        '''
            后端需要在这里改代码，保存传进来的数据到数据库，并返回正确的dict
        '''
        id = request.GET.get('id')
        account = stu.idToAccountStudent(str(id))

        info_dict = request.POST.copy()
        for i in range(1, 7):
            if info_dict['majorSelect' + str(i)].strip() == '':
                info_dict['majorSelect' + str(i)] = '0'
                print i, 909090
        for i in range(1, 4):
            if info_dict['testScore' + str(i)].strip() == '':
                info_dict['testScore' + str(i)] = '0'
        for i in range(1, 4):
            if info_dict['rank' + str(i)].strip() == '':
                info_dict['rank' + str(i)] = '0'
        for i in range(1, 4):
            if info_dict['rank' + str(i)].strip() == '':
                info_dict['rank' + str(i)] = '0'
        for i in range(1, 4):
            if info_dict['rank' + str(i) + str(i)].strip() == '':
                info_dict['rank' + str(i) + str(i)] = '0'
        if info_dict['estimateScore'].strip() == '':
            info_dict['estimateScore'] = '0'
        if info_dict['realScore'].strip() == '':
            info_dict['realScore'] = '0'
        if info_dict['admissionStatus'].strip() == '':
            info_dict['admissionStatus'] = '0'

        print info_dict
        dic = {
            'type': int(info_dict.get('type', '110')),
            'province': int(info_dict.get('province', '110')),
            'phone': info_dict.get('phone', '110'),
            'email': info_dict.get('email', '110'),
            'address': info_dict.get('address', '110'),
            'dadName': info_dict.get('dadName', '110'),
            'dadPhone': info_dict.get('dadPhone', '110'),
            'momName': info_dict.get('momName', '110'),
            'momPhone': info_dict.get('momPhone', '110'),
            'school': info_dict.get('school', '110'),
            'stu_class': info_dict.get('stu_class', '110'),
            'tutorName': info_dict.get('tutorName', '110'),
            'tutorPhone': info_dict.get('tutorPhone', '110'),
            'majorSelect1': int(info_dict.get('majorSelect1', '110')),
            'majorSelect2': int(info_dict.get('majorSelect2', '110')),
            'majorSelect3': int(info_dict.get('majorSelect3', '110')),
            'majorSelect4': int(info_dict.get('majorSelect4', '110')),
            'majorSelect5': int(info_dict.get('majorSelect5', '110')),
            'majorSelect6': int(info_dict.get('majorSelect6', '110')),
            'testScore1': int(info_dict.get('testScore1', '110')),
            'testScore2': int(info_dict.get('testScore2', '110')),
            'testScore3': int(info_dict.get('testScore3', '110')),
            'rank1': int(info_dict.get('rank1', '110')),
            'rank11': int(info_dict.get('rank11', '110')),
            'rank2': int(info_dict.get('rank2', '110')),
            'rank22': int(info_dict.get('rank22', '110')),
            'rank3': int(info_dict.get('rank3', '110')),
            'rank33': int(info_dict.get('rank33', '110')),
            'estimateScore': getStudentEstimateScore(stu.getStudentAll(account)),
            'realScore': int(info_dict.get('realScore', '110')),
            'admissionStatus': info_dict.get('admissionStatus', '110'),
            'relTeacher': info_dict.get('relTeacher', '110'),
            'relVolunteer': info_dict.get('relVolunteer', '110'),
            'comment': info_dict.get('comment', '110'),
            'team1': info_dict.get('team1', '1'),
            'team2': info_dict.get('team2', '1'),
            'team3': info_dict.get('team3', '1'),
            'team4': info_dict.get('team4', '1'),
            'team5': info_dict.get('team5', '1'),
        }

        stu.setStudent(account, Student.TYPE, dic['type'])
        stu.setStudent(account, Student.PROVINCE, dic['province'])
        stu.setStudent(account, Student.PHONE, dic['phone'])
        stu.setStudent(account, Student.EMAIL, dic['email'])
        stu.setStudent(account, Student.ADDRESS, dic['address'])
        stu.setStudent(account, Student.TYPE, dic['type'])
        stu.setStudent(account, Student.DAD_PHONE, dic['dadPhone'])
        stu.setStudent(account, Student.MOM_PHONE, dic['momPhone'])
        stu.setStudent(account, Student.SCHOOL, dic['school'])
        stu.setStudent(account, Student.CLASSROOM, dic['stu_class'])
        stu.setStudent(account, Student.TUTOR_NAME, dic['tutorName'])
        stu.setStudent(account, Student.TUTOR_PHONE, dic['tutorPhone'])
        stu.setStudent(account,
                       Student.MAJOR,
                       [dic['majorSelect1'],
                        dic['majorSelect2'],
                           dic['majorSelect3'],
                           dic['majorSelect4'],
                           dic['majorSelect5'],
                           dic['majorSelect6']])
        stu.setStudent(
            account, Student.TEST_SCORE_LIST, [
                dic['testScore1'], dic['testScore2'], dic['testScore3']])
        stu.setStudent(
            account, Student.RANK_LIST, [
                dic['rank1'], dic['rank2'], dic['rank3']])
        stu.setStudent(
            account, Student.SUM_NUMBER_LIST, [
                dic['rank11'], dic['rank22'], dic['rank33']])
        stu.setStudent(account, Student.REAL_SCORE, dic['realScore'])
        stu.setStudent(
            account,
            Student.ADMISSION_STATUS,
            dic['admissionStatus'])
        # stu.setStudent(account, Student.TYPE, dic['relTeacher'])
        # stu.setStudent(account, Student.TYPE, dic['relVolunteer'])
        stu.setStudent(account, Student.COMMENT, dic['comment'])

        stu.setStudent(account, Student.DAD_NAME, dic['dadName'])
        stu.setStudent(account, Student.MOM_NAME, dic['momName'])

        stu.setStudentGroupbyList(stu.getStudentAll(account), [dic['team1'], dic['team2'], dic['team3'],dic['team4'],dic['team5']])

        stu.setStudent(account, Student.DUIYING_TEACHER, dic['relTeacher'])
        return JsonResponse(request.POST)
    else:
        '''
            后端需要在这里改代码，从数据库读取正确的dict，并返回
        '''
        if 'user_id' not in request.session.keys():
            return redirect('/login/')
        print request.GET
        id = request.GET.get('id')
        account = stu.idToAccountStudent(str(id))
        student = stu.getStudentAll(account)
        stu_dic = stu.getStudentAllDictByAccount(account)
        dic = {
            Student.ID: stu_dic[Student.ID],
            Student.ACCOUNT: stu_dic[Student.ACCOUNT],
            Student.REAL_NAME: stu_dic[Student.REAL_NAME],
            Student.BIRTH: stu_dic[Student.BIRTH].strftime("%Y-%m-%d"),
            Student.ID_NUMBER: stu_dic[Student.ID_NUMBER],

            Student.TYPE: stu_dic[Student.TYPE],
            Student.SEX: stu_dic[Student.SEX],
            Student.NATION: stu_dic[Student.NATION],
            Student.SCHOOL: stu_dic[Student.SCHOOL],
            Student.CLASSROOM: stu_dic[Student.CLASSROOM],

            Student.ADDRESS: stu_dic[Student.ADDRESS],
            Student.PHONE: stu_dic[Student.PHONE],
            Student.EMAIL: stu_dic[Student.EMAIL],
            Student.DAD_PHONE: stu_dic[Student.DAD_PHONE],
            Student.MOM_PHONE: stu_dic[Student.MOM_PHONE],

            Student.TUTOR_NAME: stu_dic[Student.TUTOR_NAME],
            Student.TUTOR_PHONE: stu_dic[Student.TUTOR_PHONE],
            Student.PROVINCE: stu_dic[Student.PROVINCE],
            Student.MAJOR: stu_dic[Student.MAJOR],
            Student.TEST_SCORE_LIST: stu_dic[Student.TEST_SCORE_LIST],

            Student.RANK_LIST: stu_dic[Student.RANK_LIST],
            Student.SUM_NUMBER_LIST: stu_dic[Student.SUM_NUMBER_LIST],
            Student.ESTIMATE_SCORE: getStudentEstimateScore(stu.getStudentAll(account)),
            Student.REAL_SCORE: stu_dic[Student.REAL_SCORE],
            Student.REGISTER_CODE: stu_dic[Student.REGISTER_CODE],
            Student.ADMISSION_STATUS: stu_dic[Student.ADMISSION_STATUS],
            Student.TEACHER_LIST: stu_dic[Student.TEACHER_LIST],
            Student.VOLUNTEER_ACCOUNT_LIST: stu_dic[Student.VOLUNTEER_ACCOUNT_LIST],
            Student.COMMENT: stu_dic[Student.COMMENT],

            Student.MOM_NAME: stu_dic[Student.MOM_NAME],
            Student.DAD_NAME: stu_dic[Student.DAD_NAME],
            student.DUIYING_TEACHER: stu_dic[Student.DUIYING_TEACHER],
        }

        group_list = stu.getStudentGroupIDListString(student).split(' ')
        for i in range(1, 6):
            if i < len(group_list):
                dic['group'+str(i)] = group_list[i]
            else:
                dic['group'+str(i)] = '0'

        dic['grouplist'] = [' ']
        all_group = back.getGroupbyDict({})
        for item in all_group:
            dic['grouplist'].append(back.getGroupAllDictByObject(item)['id'])
        id_ = request.session.get('user_id', -1)
        return render(request,
                      'teacher/student_info_edit.html',
                      {'student': dic, 'id': id_})


@csrf_exempt
def student_info_save(request):
    t = get_template('teacher/student_info.html')
    print '------------------------'
    print 'lihaoyang : ' + str(request.POST)
    if id == -1:
        return HttpResponse('Access denied')
    account = stu.idToAccountStudent(str(id))
    stu_dic = stu.getStudentAllDictByAccount(account)
    dic = {
        Student.ID: stu_dic[Student.ID],
        Student.ACCOUNT: stu_dic[Student.ACCOUNT],
        Student.REAL_NAME: stu_dic[Student.REAL_NAME],
        Student.BIRTH: stu_dic[Student.BIRTH].strftime("%Y-%m-%d"),
        Student.ID_NUMBER: stu_dic[Student.ID_NUMBER],

        Student.TYPE: stu_dic[Student.TYPE],
        Student.SEX: stu_dic[Student.SEX],
        Student.NATION: stu_dic[Student.NATION],
        Student.SCHOOL: stu_dic[Student.SCHOOL],
        Student.CLASSROOM: stu_dic[Student.CLASSROOM],

        Student.ADDRESS: stu_dic[Student.ADDRESS],
        Student.PHONE: stu_dic[Student.PHONE],
        Student.EMAIL: stu_dic[Student.EMAIL],
        Student.DAD_PHONE: stu_dic[Student.DAD_PHONE],
        Student.MOM_PHONE: stu_dic[Student.MOM_PHONE],

        Student.TUTOR_NAME: stu_dic[Student.TUTOR_NAME],
        Student.TUTOR_PHONE: stu_dic[Student.TUTOR_PHONE],
        Student.PROVINCE: stu_dic[Student.PROVINCE],
        Student.MAJOR: stu_dic[Student.MAJOR],
        Student.TEST_SCORE_LIST: stu_dic[Student.TEST_SCORE_LIST],

        Student.RANK_LIST: stu_dic[Student.RANK_LIST],
        Student.SUM_NUMBER_LIST: stu_dic[Student.SUM_NUMBER_LIST],
        Student.ESTIMATE_SCORE: getStudentEstimateScore(stu.getStudentAll(account)),
        Student.REAL_SCORE: stu_dic[Student.REAL_SCORE],
        Student.REGISTER_CODE: stu_dic[Student.REGISTER_CODE],
        Student.ADMISSION_STATUS: stu_dic[Student.ADMISSION_STATUS],
        Student.TEACHER_LIST: stu_dic[Student.TEACHER_LIST],
        Student.VOLUNTEER_ACCOUNT_LIST: stu_dic[Student.VOLUNTEER_ACCOUNT_LIST],
        Student.COMMENT: stu_dic[Student.COMMENT],

        Student.MOM_NAME: stu_dic[Student.MOM_NAME],
        Student.DAD_NAME: stu_dic[Student.DAD_NAME],
    }

    id_ = request.session.get('user_id', -1)
    return HttpResponse(t.render({'student': dic, 'id':id_}))


def student_info_show(request):
    t = get_template('teacher/student_info.html')
    id = request.GET.get('id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    account = stu.idToAccountStudent(str(id))
    stu_dic = stu.getStudentAllDictByAccount(account)
    dic = {
        Student.ID: stu_dic[Student.ID],
        Student.ACCOUNT: stu_dic[Student.ACCOUNT],
        Student.REAL_NAME: stu_dic[Student.REAL_NAME],
        Student.BIRTH: stu_dic[Student.BIRTH].strftime("%Y-%m-%d"),
        Student.ID_NUMBER: stu_dic[Student.ID_NUMBER],

        Student.TYPE: stu_dic[Student.TYPE],
        Student.SEX: stu_dic[Student.SEX],
        Student.NATION: stu_dic[Student.NATION],
        Student.SCHOOL: stu_dic[Student.SCHOOL],
        Student.CLASSROOM: stu_dic[Student.CLASSROOM],

        Student.ADDRESS: stu_dic[Student.ADDRESS],
        Student.PHONE: stu_dic[Student.PHONE],
        Student.EMAIL: stu_dic[Student.EMAIL],
        Student.DAD_PHONE: stu_dic[Student.DAD_PHONE],
        Student.MOM_PHONE: stu_dic[Student.MOM_PHONE],

        Student.TUTOR_NAME: stu_dic[Student.TUTOR_NAME],
        Student.TUTOR_PHONE: stu_dic[Student.TUTOR_PHONE],
        Student.PROVINCE: stu_dic[Student.PROVINCE],
        Student.MAJOR: stu_dic[Student.MAJOR],
        Student.TEST_SCORE_LIST: stu_dic[Student.TEST_SCORE_LIST],

        Student.RANK_LIST: stu_dic[Student.RANK_LIST],
        Student.SUM_NUMBER_LIST: stu_dic[Student.SUM_NUMBER_LIST],
        Student.ESTIMATE_SCORE: getStudentEstimateScore(stu.getStudentAll(account)),
        Student.REAL_SCORE: stu_dic[Student.REAL_SCORE],
        Student.REGISTER_CODE: stu_dic[Student.REGISTER_CODE],
        Student.ADMISSION_STATUS: stu_dic[Student.ADMISSION_STATUS],
        Student.TEACHER_LIST: stu_dic[Student.TEACHER_LIST],
        Student.VOLUNTEER_ACCOUNT_LIST: stu_dic[Student.VOLUNTEER_ACCOUNT_LIST],
        Student.COMMENT: stu_dic[Student.COMMENT],

        Student.MOM_NAME: stu_dic[Student.MOM_NAME],
        Student.DAD_NAME: stu_dic[Student.DAD_NAME],
        Student.DUIYING_TEACHER: stu_dic[Student.DUIYING_TEACHER],
    }

    group_list = stu.getStudentGroupIDListString(stu.getStudentAll(account)).split(' ')
    for i in range(1, 6):
        if i < len(group_list):
            dic['group' + str(i)] = group_list[i]
        else:
            dic['group' + str(i)] = '0'

    dic['grouplist'] = [' ']
    all_group = back.getGroupbyDict({})
    for item in all_group:
        dic['grouplist'].append(back.getGroupAllDictByObject(item)['id'])
    print dic['grouplist']

    id_ = request.session.get('user_id', -1)
    return HttpResponse(t.render({'student': dic, 'id':id_}))


@ensure_csrf_cookie
def add_student(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('teacher/add_student.html')
    c = {'id': id}
    return HttpResponse(t.render(c))


def fake_backend(request):
    if request.is_ajax() and request.method == 'POST':
        c = {
            'name': 'Alice',
            'gender': '男',
            'source': '北京',
            'school': '人大附中',
            'id_card': '11010819980824181X'}
        c['name'] = request.POST.get('name')
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


def dashboard(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('teacher/dashboard.html')
    c = {'id': id}
    return HttpResponse(t.render(c))


def add_volunteer(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('teacher/add_volunteer.html')
    c = {'id': id}
    return HttpResponse(t.render(c))


'''
		查看和修改教师个人信息
		by byr 161012
'''
# @csrf_protect
@csrf_exempt
def profile(request):
    if request.method == 'POST':
        '''
            后端需要在这里改代码，保存传进来的数据到数据库，并返回正确的dict
        '''
        password1 = request.POST.get('password', 'byr')
        teacher_name = request.POST.get('teacher_name', 'byr')
        phone = request.POST.get('phone', '110')
        email = request.POST.get('email', '110')
        work_address = request.POST.get('work_address', '110')
        describe = request.POST.get('describe', '110')
        # The default values above are not making any difference
        # You are only covering up bugs if there are any
        # You should check the keys like:
        # try:
        #   teacher_name = request.POST.get('teacher_name')
        # except KeyError:
        #   dosomething()
        # by dqn14 2016/11/1

        id = (int)(request.session.get('user_id'))
        account = tch.idToAccountTeacher(id)

        tch.setTeacher(account, Teacher.REAL_NAME, teacher_name)
        tch.setTeacher(account, Teacher.PHONE, phone)
        tch.setTeacher(account, Teacher.EMAIL, email)
        tch.setTeacher(account, Teacher.AREA, work_address)
        tch.setTeacher(account, Teacher.COMMENT, describe)
        tch.setTeacher(account, Teacher.PASSWORD, password1)

        return JsonResponse(request.POST)
    else:
        '''
            后端需要在这里改代码，从数据库读取正确的dict，并返回
        '''
        id = (str)(request.session.get('user_id'))
        account = tch.idToAccountTeacher(id)
        teacher = tch.getTeacherAll(account)
        dict = {
            'user_name': getattr(teacher, Teacher.ACCOUNT, ' '),
            'teacher_name': getattr(teacher, Teacher.REAL_NAME, ' '),
            'email': getattr(teacher, Teacher.EMAIL, ' '),
            'work_address': getattr(teacher, Teacher.AREA, ' '),
            'phone': getattr(teacher, Teacher.PHONE, ' '),
            'describe': getattr(teacher, Teacher.COMMENT, ' '),
            'password1': getattr(teacher, Teacher.PASSWORD, 'password'),
            'password2': getattr(teacher, Teacher.PASSWORD, 'password'),
        }
        #print 'dict ',dict
        # No garbage output
        # by dqn14 2016/11/1
        return render(request, 'teacher/userinfo.html', {'dict': dict, 'id':id})

'''
    上传图片处理
    by byr 161025
'''
def handle_uploaded_img(imgFile, year, province, subject, number, score, category):
    imgName = imgFile.name
    path = 'student/static/images/'+ get_picture_path(year, province, subject, number, score, category)
    dst = open(path, 'wb')
    dst.write(imgFile.read())


'''
		老师上传试题
		by byr 161016
'''
@csrf_exempt
def upload(request):
    if request.method == 'GET':
        id = request.GET.get('test_id')
        num = int(request.GET.get('num'))
        list = id.split('_')
        year = find_item_index_in_list(int(list[0]), YEAR_LIST)
        province = find_item_index_in_list(list[1], SHITI_LIST)
        subject = find_item_index_in_list(list[2], SUBJECT_LIST)
        dic = {
            'year': {'year': year, 'yearlist': YEAR_LIST},
            'province': {'province': province, 'provincelist': PROVINCE_LIST},
            'subject': {'subject': subject, 'subjectlist': SUBJECT_LIST},
            'number': {'number': num, 'numberlist': NUMBER_LIST},
            'score': {'score': 0, 'scorelist': SCORE_LIST},
            'category': {'category': 0, 'categorylist': CATEGORY_LIST},
        }
        id_ = request.session.get('user_id', -1)
        return render(request, 'teacher/uploadtest.html', {'dict': dic, 'id':id_})
    else:
        year = request.POST.get('year')
        province = request.POST.get('province')
        subject = request.POST.get('subject')
        number = request.POST.get('number')
        score = request.POST.get('score')
        category = request.POST.get('category')

        print year, province, subject, number, score, category

        dic = {
            Picture.YEAR: int(year),
            Picture.PROVINCE: int(province),
            Picture.SUBJECT: int(subject),
            Picture.NUMBER: int(number),
            Picture.SCORE: int(score),
            Picture.CATEGORY: int(category),
        }

        flag = pic.createPicturebyDict(dic)
        imgFile = request.FILES['problem_upload']
        handle_uploaded_img(imgFile, year, province, subject, number, score, category)



        if flag:
            dict = {'result': '上传成功'}
        else:
            dict = {'result': '上传失败'}
        return JsonResponse(dict)


'''
		老师查看志愿者详情
		by byr 161017
'''
@csrf_exempt
def volunteer_info(request):
    '''
    后端需要在这里获取数据并返回
    '''
    if 'user_id' not in request.session.keys():
        return redirect('/login/')
    id = request.GET.get('id')
    print request.GET
    account = vol.idToAccountVolunteer(str(id))
    volunteer = vol.getVolunteerAll(account)

    vol_dic = vol.getVolunteerAllDictByAccount(account)

    dict = {
        'id': vol_dic[Volunteer.ID],
        'user_name': vol_dic[Volunteer.ACCOUNT],
        'realName': vol_dic[Volunteer.REAL_NAME],
        'idNumber': vol_dic[Volunteer.ID_NUMBER],
        'sex': vol_dic[Volunteer.SEX],
        'nation': vol_dic[Volunteer.NATION],
        'birth_year': vol_dic[Volunteer.BIRTH].strftime("%Y"),
        'birth_month': vol_dic[Volunteer.BIRTH].strftime("%m"),
        'birth_date': vol_dic[Volunteer.BIRTH].strftime("%d"),
        'department': vol_dic[Volunteer.MAJOR][0],
        'class': vol_dic[Volunteer.CLASSROOM],
        'phone': vol_dic[Volunteer.PHONE],
        'email': vol_dic[Volunteer.EMAIL],
        'province': vol_dic[Volunteer.PROVINCE],
        'distribute': '1 | 2 | 3',
        'qqn': vol_dic[Volunteer.QQ],
        'weichat': vol_dic[Volunteer.WECHAT],
        'teacher': '白老师 | 李老师',
        'comment': vol_dic[Volunteer.COMMENT],
    }
    id_ = request.session.get('user_id', -1)
    return render(request, 'teacher/volunteer_info.html', {'dict': dict, 'id':id_})


'''
		老师编辑志愿者详情
		by byr 161017
'''
@csrf_exempt
def volunteer_info_edit(request):
    if request.method == 'POST':
        '''
            后端需要在这里改代码，保存传进来的数据到数据库，并返回正确的dict
        '''
        id = request.GET.get('id')
        account = vol.idToAccountVolunteer(str(id))
        volunteer = vol.getVolunteerAll(account)

        # 志愿者页面上目前可以修改的，之后会在有所改动
        phone = request.POST.get('phone', '110')
        email = request.POST.get('email', '110@qq')
        weichat = request.POST.get('weichat', '110@qq')
        comment = request.POST.get('comment', '110')
        qqn = request.POST.get('qqn', '110')

        vol.setVolunteer(account, Volunteer.PHONE, phone)
        vol.setVolunteer(account, Volunteer.EMAIL, email)
        vol.setVolunteer(account, Volunteer.WECHAT, weichat)
        vol.setVolunteer(account, Volunteer.COMMENT, comment)
        vol.setVolunteer(account, Volunteer.QQ, qqn)
        vol.setVolunteerGroupbyList(volunteer, [10,9,8])

        return JsonResponse(request.POST)
    else:
        '''
            后端需要在这里改代码，从数据库读取正确的dict，并返回
        '''
        if 'user_id' not in request.session.keys():
            return redirect('/login/')
        print request.GET
        id = request.GET.get('id')
        account = vol.idToAccountVolunteer(str(id))
        volunteer = vol.getVolunteerAll(account)
        vol_dic = vol.getVolunteerAllDictByAccount(account)
        dic = {
            'id': vol_dic[Volunteer.ID],
            'user_name': vol_dic[Volunteer.ACCOUNT],
            'realName': vol_dic[Volunteer.REAL_NAME],
            'idNumber': vol_dic[Volunteer.ID_NUMBER],
            'sex': vol_dic[Volunteer.SEX],
            'nation': vol_dic[Volunteer.NATION],
            'birth_year': vol_dic[Volunteer.BIRTH].strftime("%Y"),
            'birth_month': vol_dic[Volunteer.BIRTH].strftime("%m"),
            'birth_date': vol_dic[Volunteer.BIRTH].strftime("%d"),
            'department': vol_dic[Volunteer.MAJOR][0],
            'class': vol_dic[Volunteer.CLASSROOM],
            'phone': vol_dic[Volunteer.PHONE],
            'email': vol_dic[Volunteer.EMAIL],
            'province': vol_dic[Volunteer.PROVINCE],
            'distribute': '1 | 2 | 3',
            'qqn': vol_dic[Volunteer.QQ],
            'weichat': vol_dic[Volunteer.WECHAT],
            'teacher': '白老师 | 李老师',
            'comment': vol_dic[Volunteer.COMMENT],
        }

        group_list = vol.getVolunteerGroupIDListString(volunteer).split(' ')
        for i in range(1, 6):
            if i < len(group_list):
                dic['group' + str(i)] = group_list[i]
            else:
                dic['group' + str(i)] = '0'

        dic['grouplist'] = [' ']
        all_group = back.getGroupbyDict({})
        for item in all_group:
            dic['grouplist'].append(back.getGroupAllDictByObject(item)['id'])

        id_ = request.session.get('user_id', -1)
        return render(request,
                      'teacher/volunteer_info_edit.html',
                      {'dict': dic, 'id':id_})


'''
		老师给学生分组
		by byr 161017
'''
def distribute_student(request):
    '''
       GET newteam 新建组
    '''
    if 'newteam' in request.GET:
        back.createGroupbyDict({Group.NAME: 'new name'})
        num = len(back.getGroupbyDict({}))
        return JsonResponse({'teamnum': num})
    '''
    GET id teamid 删除
    '''
    if ('id' in request.GET) and ('teamid' in request.GET)and ('class' in request.GET):

        print 'cao ', request.GET
        group_id = int(request.GET['teamid'])
        isDelStudent = int(request.GET['class'])
        if isDelStudent == 1:
            stu_id = str(request.GET['id'])
            group = back.getGroupbyDict({Group.ID: group_id})[0]
            group_dic = back.getGroupAllDictByObject(group)
            # print 'group_dic', group_dic
            stu_id_list = group_dic[Group.STU_LIST].split('_')
            if stu_id in stu_id_list:
                stu_id_list.remove(stu_id)
            str_list = '_'.join(stu_id_list)
            print 'haha', str_list
            back.setGroup(group, Group.STU_LIST, str_list)
        else:
            vol_id = str(request.GET['id'])
            group = back.getGroupbyDict({Group.ID: group_id})[0]
            group_dic = back.getGroupAllDictByObject(group)
            vol_id_list = group_dic[Group.VOL_LIST].split('_')
            if vol_id in vol_id_list:
                vol_id_list.remove(vol_id)
            str_list = '_'.join(vol_id_list)
            back.setGroup(group, Group.VOL_LIST, str_list)

        return JsonResponse({'success': 1})
    else:
        team_list = []

        group_list = back.getGroupbyDict({})
        for group in group_list:
            group_dic = back.getGroupAllDictByObject(group)
            team = {}
            team['teamleader'] = str(group_dic[Group.ID])
            team['teamname'] = str(group_dic[Group.NAME])
            team['volunteer'] = {}
            team['student'] = {}

            print 'adf', group_dic
            if len(group_dic[Group.VOL_LIST].strip()) > 0:
                vol_id_list = group_dic[Group.VOL_LIST].split('_')
                for i in range(0, len(vol_id_list)):
                    if vol_id_list[i].strip() == '':
                        continue
                    vol_account = vol.idToAccountVolunteer(str(vol_id_list[i]))
                    vol_dic = vol.getVolunteerAllDictByAccount(vol_account)
                    dic = {
                        'user_name': vol_dic[Volunteer.ACCOUNT],
                        'name': vol_dic[Volunteer.REAL_NAME],
                        'id': vol_dic[Volunteer.ID],
                    }
                    team['volunteer'][('volunteer' + str(i))] = dic

            if len(group_dic[Group.STU_LIST].strip()) > 0:
                stu_id_list = group_dic[Group.STU_LIST].split('_')
                for i in range(0, len(stu_id_list)):
                    if stu_id_list[i].strip() == '':
                        continue
                    stu_account = stu.idToAccountStudent(str(stu_id_list[i]))
                    stu_dic = stu.getStudentAllDictByAccount(stu_account)
                    dic = {
                        'user_name': stu_dic[Student.ACCOUNT],
                        'name': stu_dic[Student.REAL_NAME],
                        'id': stu_dic[Student.ID],
                    }
                    team['student'][('student' + str(i))] = dic

            team_list.append(team)
        team_list.reverse()

        id_ = request.session.get('user_id', -1)
        return render(request,
                      'teacher/distribute_student.html',
                      {'dict': team_list, 'id':id_})



            
def download_registration_xls(request, file_name):
    file_path = os.path.join('files', file_name)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name)
    return response
    
def view_message(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('teacher/view_message.html')
    c = {'id': id}
    return HttpResponse(t.render(c))
    
def manage_test(request):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('teacher/view_test.html')
    c = {'id': id}
    return HttpResponse(t.render(c))
    
def edit_test(request, test_id):
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('teacher/edit_test.html')
    c = {'id': id, 'test_id': test_id}
    return HttpResponse(t.render(c))

@csrf_exempt
def checkscore(request):
    '''

    后端需要从数据库获取数据补全代码
    '''
    list = []
    student_list = stu.getAllInStudent()
    for student in student_list:
        info_dic = stu.getStudentAllDictByAccount(getattr(student, Student.ACCOUNT))
        name = info_dic[Student.REAL_NAME]
        sex = SEX_LIST[int(info_dic[Student.SEX]['sex'])]
        province = PROVINCE_LIST[int(info_dic[Student.PROVINCE]['province'])]
        school = info_dic[Student.SCHOOL]
        ident = info_dic[Student.ID_NUMBER]
        estimate_score = info_dic[Student.ESTIMATE_SCORE]
        try:
            estimate_score = eval(estimate_score)
        except:
            estimate_score = eval('{}')
        for key in estimate_score.keys():
            testname = key
            time = str(estimate_score[key]['time']) + ' s'
            score = str(estimate_score[key]['score']) + ' points'
            if 'shenhe' in estimate_score[key].keys():
                continue
            else:
                dict = {'name':name,
                        'sex': sex,
                        'province': province,
                        'school':school,
                        'ident': ident,
                        'testname': testname,
                        'time': time,
                         'score':score,
                }
                list.append(dict)

    id_ = request.session.get('user_id', -1)
    return render(request,
                  'teacher/checkscore.html', {'dict':list, 'id':id_})