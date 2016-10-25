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
import database.image_backend as pic
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
		c = {'id': id}
		return HttpResponse(t.render(c))


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
        for i in range(1,7):
            if info_dict['majorSelect'+str(i)] == '':
                info_dict['majorSelect'+str(i)] = '0'
                print i,909090
        for i in range(1,4):
            if info_dict['testScore'+str(i)] == '':
                info_dict['testScore'+str(i)] = '0'
        for i in range(1,4):
            if info_dict['rank'+str(i)] == '':
                info_dict['rank'+str(i)] = '0'
        for i in range(1,4):
            if info_dict['rank'+str(i)] == '':
                info_dict['rank'+str(i)] = '0'
        for i in range(1,4):
            if info_dict['rank'+str(i)+str(i)] == '':
                info_dict['rank'+str(i)+str(i)] = '0'
        if info_dict['estimateScore'] == '':
            info_dict['estimateScore'] = '0'
        if info_dict['realScore'] == '':
            info_dict['realScore'] = '0'
        if info_dict['admissionStatus'] == '':
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
            'estimateScore': int(info_dict.get('estimateScore', '110')),
            'realScore': int(info_dict.get('realScore', '110')),
            'admissionStatus': int(info_dict.get('admissionStatus', '110')),
            'relTeacher': info_dict.get('relTeacher', '110'),
            'relVolunteer': info_dict.get('relVolunteer', '110'),
            'comment': info_dict.get('comment', '110'),
        }

        stu.setStudent(account, Student.TYPE, dic['type'])
        stu.setStudent(account, Student.PROVINCE, dic['province'])
        stu.setStudent(account, Student.PHONE, dic['phone'])
        stu.setStudent(account, Student.EMAIL, dic['email'])
        stu.setStudent(account, Student.ADDRESS, dic['address'])
        stu.setStudent(account, Student.TYPE, dic['dadName'])
        stu.setStudent(account, Student.DAD_PHONE, dic['dadPhone'])
        stu.setStudent(account, Student.TYPE, dic['momName'])
        stu.setStudent(account, Student.MOM_PHONE, dic['momPhone'])
        stu.setStudent(account, Student.SCHOOL, dic['school'])
        stu.setStudent(account, Student.CLASSROOM, dic['stu_class'])
        stu.setStudent(account, Student.TUTOR_NAME, dic['tutorName'])
        stu.setStudent(account, Student.TUTOR_PHONE, dic['tutorPhone'])
        stu.setStudent(account, Student.MAJOR, [dic['majorSelect1'], dic['majorSelect2'], dic['majorSelect3'],
                       dic['majorSelect4'], dic['majorSelect5'], dic['majorSelect6']] )
        stu.setStudent(account, Student.TEST_SCORE_LIST, [dic['testScore1'], dic['testScore2'], dic['testScore3']] )
        stu.setStudent(account, Student.RANK_LIST, [dic['rank1'], dic['rank2'], dic['rank3']])
        stu.setStudent(account, Student.SUM_NUMBER_LIST, [dic['rank11'], dic['rank22'], dic['rank33']])
        stu.setStudent(account, Student.ESTIMATE_SCORE, dic['estimateScore'])
        stu.setStudent(account, Student.REAL_SCORE, dic['realScore'])
        stu.setStudent(account, Student.ADMISSION_STATUS, dic['admissionStatus'])
        stu.setStudent(account, Student.TYPE, dic['relTeacher'])
        stu.setStudent(account, Student.TYPE, dic['relVolunteer'])
        stu.setStudent(account, Student.COMMENT, dic['comment'])


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

        # 这里的写法不是很好，但是前端的设计太不科学了只能这样了
        majorList = stu_dic[Student.MAJOR]
        testScoreList = stu_dic[Student.TEST_SCORE_LIST]
        rankList = stu_dic[Student.RANK_LIST]
        sumNumberList = stu_dic[Student.SUM_NUMBER_LIST]
        for i in range(0, 10):
            majorList.append('')
            testScoreList.append('')
            rankList.append('')
            sumNumberList.append('')
        # 就吐槽前端到这里吧，前端也不容易

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
            Student.ESTIMATE_SCORE: stu_dic[Student.ESTIMATE_SCORE],
            Student.REAL_SCORE: stu_dic[Student.REAL_SCORE],
            Student.REGISTER_CODE: stu_dic[Student.REGISTER_CODE],
            Student.ADMISSION_STATUS: stu_dic[Student.ADMISSION_STATUS],
            Student.TEACHER_LIST: stu_dic[Student.TEACHER_LIST],
            Student.VOLUNTEER_ACCOUNT_LIST: stu_dic[Student.VOLUNTEER_ACCOUNT_LIST],
            Student.COMMENT: stu_dic[Student.COMMENT],
        }
        print Student.TEST_SCORE_LIST, stu_dic[Student.TEST_SCORE_LIST],'caocao'
        return render(request, 'teacher/student_info_edit.html', {'student': dic})

@csrf_exempt
def student_info_save(request):
    t = get_template('teacher/student_info.html')
    print '------------------------'
    print 'lihaoyang : ' + str(request.POST)
    if id == -1:
        return HttpResponse('Access denied')
    account = stu.idToAccountStudent(str(id))
    student = stu.getStudentAll(account)

    return HttpResponse(t.render({'student': dic}))


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
        Student.ESTIMATE_SCORE: stu_dic[Student.ESTIMATE_SCORE],
        Student.REAL_SCORE: stu_dic[Student.REAL_SCORE],
        Student.REGISTER_CODE: stu_dic[Student.REGISTER_CODE],
        Student.ADMISSION_STATUS: stu_dic[Student.ADMISSION_STATUS],
        Student.TEACHER_LIST: stu_dic[Student.TEACHER_LIST],
        Student.VOLUNTEER_ACCOUNT_LIST: stu_dic[Student.VOLUNTEER_ACCOUNT_LIST],
        Student.COMMENT: stu_dic[Student.COMMENT],
    }
    return HttpResponse(t.render({'student': dic}))


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
        c = {'name': 'Alice', 'gender': '男', 'source': '北京', 'school': '人大附中', 'id_card': '11010819980824181X'}
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
            'teacher_name': getattr(teacher, Teacher.REAL_NAME, 'no such attr. by lihy'),
            'email': getattr(teacher, Teacher.EMAIL, 'no such attr. by lihy'),
            'work_address': getattr(teacher, Teacher.AREA, 'no such attr. by lihy'),
            'home_address': '130',
            'postcode': '43',
            'homephone': '120',
            'phone': getattr(teacher, Teacher.PHONE, 'no such attr. by lihy'),
            'qqn': '85',
            'weichat': '66',
            'describe': '57',
        }
        return render(request, 'teacher/userinfo.html', {'dict': dict})

'''
    上传图片处理
    by byr 161025
'''
def handle_uploaded_img(imgFile):
    imgName = imgFile.name
    dst = open(imgName, 'wb')
    dst.write(imgFile.read())
#    for chunk in imgFile.chunks():
#        dst.write(chunk)
#        dst.close()



'''
		老师上传试题
		by byr 161016
'''
@csrf_exempt
def upload(request):
    print '-----------'
    print request.POST
    if (request.method == 'GET'):
        return render(request, 'teacher/uploadtest.html')
    else:
        imgFile = request.FILES['problem_upload']
        handle_uploaded_img(imgFile)


        form = pic.ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # m = Picture.objects.get(pk=course_id)
            # m.model_pic = form.cleaned_data['image']
            # m.save()
            print pic.createPicture('a', {Picture.IMG: form.cleaned_data['image']})
        else:
            print 'hahahahahah'
        dict = {'result': '上传成功'}
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
        'user_name': vol_dic[Volunteer.REAL_NAME],
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
        'qqn': '123456789',
        'weichat': vol_dic[Volunteer.WECHAT],
        'teacher': '白老师 | 李老师',
        'comment': vol_dic[Volunteer.COMMENT],
    }
    print vol_dic[Volunteer.MAJOR][0]
    return render(request, 'teacher/volunteer_info.html', {'dict': dict})


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

        vol.setVolunteer(account, Volunteer.PHONE, phone)
        vol.setVolunteer(account, Volunteer.EMAIL, email)
        vol.setVolunteer(account, Volunteer.WECHAT, weichat)
        vol.setVolunteer(account, Volunteer.COMMENT, comment)

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
        dict = {
            'id': vol_dic[Volunteer.ID],
            'user_name': vol_dic[Volunteer.REAL_NAME],
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
            'qqn': '123456789',
            'weichat': vol_dic[Volunteer.WECHAT],
            'teacher': '白老师 | 李老师',
            'comment': vol_dic[Volunteer.COMMENT],
        }
        return render(request, 'teacher/volunteer_info_edit.html', {'dict': dict})


'''
		老师给学生分组
		by byr 161017
'''


def distribute_student(request):
    if 'id' not in request.GET:
        # student = {
        #     'user_name':'ligoupang',
        #     'name':'李狗胖',
        #     'id':'233',
        # }
        # team1 = {'teamleader': 李狗胖,
        #           'teamname':2,
        #         'student1': student,
        #         'student2': student,
        #         'student3': student,
        #         'student4': student,
        #         'student5': student,
        #         }
        # team2 = {'teamname': 3,
        #         'student1': student,
        #         'student2': student,
        #         'student3': student,
        #         'student4': student,
        #         'student5': student,
        #         }
        # team3 = {'teamname': 4,
        #         'student1': student,
        #         'student2': student,
        #         'student3': student,
        #         'student4': student,
        #         'student5': student,
        #         }
        # team = {'teamname': 1,
        #         'student1': student,
        #         'student2': student,
        #         'student3': student,
        #         'student4': student,
        #         'student5': student,
        #         }
        # dict = [team, team1, team2, team3]
        team_list = []
        vol_all = vol.getAllInVolunteer()
        for vol_item in vol_all:
            vol_stu_account_list = getattr(vol_item, Volunteer.STUDENT_ACCOUNT_LIST)
            team = {}
            team['teamleader'] = getattr(vol_item, Volunteer.REAL_NAME)
            team['teamname'] = getattr(vol_item, Volunteer.ACCOUNT)
            for i in range(0, len(vol_stu_account_list)):
                student = stu.getStudentAll(vol_stu_account_list[i])
                dic = {
                    'user_name': getattr(student, Student.ACCOUNT, 'NO'),
                    'name': getattr(student, Student.REAL_NAME, 'NO'),
                    'id': getattr(student, Student.ID, 'NO'),
                }
                team[('student' + str(i))] = dic
            team_list.append(team)
        return render(request, 'teacher/distribute_student.html', {'dict': team_list})
    else:
        vol_id = 2
        stu_id = request.GET['id']
        volunteer_account = vol.idToAccountVolunteer(str(vol_id))
        student_account = stu.idToAccountStudent(str(stu_id))

        print volunteer_account
        print student_account
        vol_de_stu_account_list = vol.getVolunteerAllDictByAccount(volunteer_account)[Volunteer.STUDENT_ACCOUNT_LIST]
        stu_de_vol_account_list = stu.getStudentAllDictByAccount(student_account)[Student.VOLUNTEER_ACCOUNT_LIST]

        print vol_de_stu_account_list
        print stu_de_vol_account_list
        vol_de_stu_account_list.remove(student_account)
        stu_de_vol_account_list.remove(volunteer_account)
        print vol_de_stu_account_list
        print stu_de_vol_account_list

        flag1 = vol.setVolunteer(volunteer_account, Volunteer.STUDENT_ACCOUNT_LIST, vol_de_stu_account_list)
        flag2 = stu.setStudent(student_account, Student.VOLUNTEER_ACCOUNT_LIST, stu_de_vol_account_list)

        if flag1 and flag2:
            return JsonResponse({'success': 1})
        else:
            return JsonResponse({'success': 0})

