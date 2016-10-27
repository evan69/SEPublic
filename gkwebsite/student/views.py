#encoding=utf-8
from django.http import JsonResponse
from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect
import datetime


# Create your views here.

def student_center(request):
    t = get_template('student/center.html')
    id = request.session.get('user_id', -1)
    c = {'id': id}
    return HttpResponse(t.render(c))


def student_score(request):
    t = get_template('student/score.html')
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    c = {'id': id}
    return HttpResponse(t.render(c))


def student_rank(request):
    t = get_template('student/rank.html')
    return HttpResponse(t.render({}))


def student_admit(request):
    t = get_template('student/admit.html')
    return HttpResponse(t.render({}))


def student_contact(request):
    t = get_template('student/contact.html')
    return HttpResponse(t.render({}))


def student_logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('/login')


def profile(request):
    dict = {
        'name': 'name',
        'identification': 'identification',
        'sex': 'sex',
        'nation': 'nation',
        'birth': 'birth',
        'province': 'province',
        'phone': 'phone',
        'email': 'email',
        'wenli': 'wenli',
        'address': 'address',
        'dadName': 'dadName',
        'dadPhone': 'dadPhone',
        'momName': 'momName',
        'momPhone': 'momPhone',
        'school': 'school',
        'stu_class': 'stu_class',
        'tutorName': 'tutorName',
        'tutorPhone': 'tutorPhone',
        'majorSelect1': 'majorSelect1',
        'majorSelect2': 'majorSelect2',
        'majorSelect3': 'majorSelect3',
        'majorSelect4': 'majorSelect4',
        'majorSelect5': 'majorSelect5',
        'majorSelect6': 'majorSelect6',
        'testScore1': 'testScore1',
        'testScore2': 'testScore2',
        'testScore3': 'testScore3',
        'rank1': 'rank1',
        'rank11': 'rank11',
        'rank2': 'rank2',
        'rank22': 'rank22',
        'rank3': 'rank3',
        'rank33': 'rank33',
                        'realScore': 'realScore',
                          'relTeacher': 'relTeacher',
                       'comment': 'comment',
    }
    if request.method == 'POST':
        '''
        保存信息并返回json
        '''
        return JsonResponse(dict)
    else:
        '''
        获取信息并返回
        '''
        return render(request, 'student/userinfo.html', {'dict':dict})
