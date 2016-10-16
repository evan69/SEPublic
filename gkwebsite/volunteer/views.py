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
from database.models import *

# Create your views here.

@ensure_csrf_cookie
def search_student(request):
    # for debug here
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    t = get_template('volunteer/v_list_student.html')
    c = {'id': id}
    return HttpResponse(t.render(c))


def student_list_all(request):
    vol_id = request.session.get('user_id')
    vol_account = vol.idToAccountVolunteer(vol_id)
    vol_student_account_list = getattr(vol.getVolunteerAll(vol_account), Volunteer.STUDENT_ACCOUNT_LIST)

    if request.is_ajax() and request.method == 'POST':
        t = []
        for account in vol_student_account_list:
            item = stu.getStudentAll(account)
            dic = {'id': getattr(item, 'id'),
                   'name': getattr(item, Student.REAL_NAME),
                   'gender': getattr(item, Student.SEX),
                   'source': getattr(item, Student.PROVINCE),
                   'school': getattr(item, Student.SCHOOL),
                   'id_card': getattr(item, Student.ID_NUMBER)}
            t.append(dic)
        return JsonResponse(t, safe=False)  # must use 'safe=False'
    else:
        return HttpResponse('Access denied.')


def student_info_show(request):
    t = get_template('volunteer/student_info.html')
    c = Context({})
    print request.session.get('user_id')
    return HttpResponse(t.render(c))


@csrf_exempt
def profile(request):
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
