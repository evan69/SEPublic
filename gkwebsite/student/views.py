#coding:utf8
from django.shortcuts import render

from django.http import HttpResponse,JsonResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
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
    return render(request, 'student/userinfo.html')

@csrf_exempt
def get_all_tests(request):
    """
        后端应在此处返回该学生全部可以做的题目名称。名称无重复
        学生id由request.session中获取，同其他函数里的写法
        然后放到下面样例写好的dic的'tests'键对应的列表值中
    """
    dic = {'tests' : ['2016湖北语文','2017北京数学','2014四川生物']}
    return JsonResponse(dic)

@csrf_exempt
def do_test(request):
    test_name = request.GET.get('test_name')
    t = get_template('student/do_test.html')
    return HttpResponse(t.render({'test_name': test_name}))
    # return render(request, 'student/do_test.html')
    # return HttpResponse(t.render({}))

@csrf_exempt
def get_problem_list(request):
    """
        后端应在此处返回某套题内包含的题目id列表，且需要按顺序
        试题名称由request.POST.get('test_name')获取，见下面样例
        然后放到下面样例写好的dic的'problem_list'键对应的列表值中
    """
    test_name = request.POST.get('test_name')
    print test_name
    print 'problem list'
    dic = {'problem_list': [1, 5, 22]}
    return JsonResponse(dic)

@csrf_exempt
def get_problem_info(request):
    """
        后端应在此处返回某道试题的全部信息，信息应转化为字符串
        试题id由request.POST.get('problem_id')获取，见下面样例
        然后放到下面样例写好的dic中
    """
    problem_id = request.POST.get('problem_id')
    print problem_id
    print 'problem id'
    if int(problem_id) < 4:
        dic = {'problem_num': '999',
           'problem_type': '客观',
           'problem_full_score': '10',
           'problem_pic': '/static/images/2017_beijing_chinese_1_1_subjective'}
    else:
        dic = {'problem_num': '22',
           'problem_type': '主观',
           'problem_full_score': '44',
           'problem_pic': '/static/images/2017_beijing_chinese_1_1_subjective'}
    return JsonResponse({'problem_info': dic})

@csrf_exempt
def submit_test_result(request):
    """
        后端应在此处保存这次答题的结果
        学生id从request.session获取
        时间数据、分数数据、试题名称见下面样例
        返回空Json即可
    """
    print request.POST
    time_list = [int(item) for item in request.POST.get('time_list').split(",")]
    score_list = [int(item) for item in request.POST.get('score_list').split(",")]
    test_name = request.POST.get('test_name')
    print time_list
    print score_list
    print test_name
    return JsonResponse({})
