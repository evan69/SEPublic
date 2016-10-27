#coding:utf8
from django.shortcuts import render

from django.http import HttpResponse,JsonResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
import datetime

from database.models import *
from database.my_field import *
import database.student_backend as stu
import database.image_backend as pic


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


rec_dict = {}

@csrf_exempt
def get_all_tests(request):
    """
        后端应在此处返回该学生全部可以做的题目名称。名称无重复
        学生id由request.session中获取，同其他函数里的写法
        然后放到下面样例写好的dic的'tests'键对应的列表值中
    """
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    print id
    account = stu.idToAccountStudent(str(id))
    stu_dic = stu.getStudentAllDictByAccount(account)
    year = datetime.datetime.now().strftime("%Y")

    year = int(year) - YEAR_LIST[1] + 1
    province = int(stu_dic[Student.PROVINCE]['province'])

    dic = {
        Picture.YEAR: year,
        Picture.PROVINCE: province,
    }
    global rec_dict
    rec_dict = dic

    ret_list = []
    subject_list = []
    pic_list = pic.getPicturebyDict(dic)
    for item in pic_list:
        pic_dic = pic.getPictureAllDictByObject(item)
        if pic_dic[Picture.SUBJECT] in subject_list:
            continue
        subject_list.append(pic_dic[Picture.SUBJECT])
        tao = u'%s_%s_%s' % (str(YEAR_LIST[pic_dic[Picture.YEAR]]),
                            str(PROVINCE_LIST[pic_dic[Picture.PROVINCE]]),
                            str(SUBJECT_LIST[pic_dic[Picture.SUBJECT]]))
        ret_list.append(tao)


    dic = {'tests' : ret_list}

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
    # print 'test_name', test_name
    info = test_name
    info_list = info.split('_')
    print info_list
    year = int(info_list[0]) - YEAR_LIST[1] + 1
    province = find_item_index_in_list(info_list[1], PROVINCE_LIST)
    subject = find_item_index_in_list(info_list[2], SUBJECT_LIST)

    dict = {
        Picture.YEAR: year,
        Picture.PROVINCE: province,
        Picture.SUBJECT: subject,
    }

    if province == -1 or subject == -1:
        print 'ERROR !!!!!!!!!!!!!!!!!!!'

    id_list = []
    pic_list = pic.getPicturebyDict(dict)
    print 'len ', len(pic_list)
    for item in pic_list:
        pic_dic = pic.getPictureAllDictByObject(item)
        id_list.append(pic_dic[Picture.ID])

    dic = {'problem_list': id_list}
    print 'id_list ', id_list
    return JsonResponse(dic)

@csrf_exempt
def get_problem_info(request):
    """
        后端应在此处返回某道试题的全部信息，信息应转化为字符串
        试题id由request.POST.get('problem_id')获取，见下面样例
        然后放到下面样例写好的dic中
    """
    # print request.POST
    problem_id = request.POST.get('problem_id')

    picture = pic.getPicturebyField('id', int(problem_id))
    pic_dic = pic.getPictureAllDictByObject(picture[0])
    pic_name = get_picture_path(pic_dic[Picture.YEAR], pic_dic[Picture.PROVINCE],
                                pic_dic[Picture.SUBJECT], pic_dic[Picture.NUMBER],
                                pic_dic[Picture.SCORE], pic_dic[Picture.CATEGORY])
    # print pic_dic

    dic = {'problem_num': pic_dic[Picture.NUMBER],
       'problem_type': CATEGORY_LIST[pic_dic[Picture.CATEGORY]],
       'problem_full_score': pic_dic[Picture.SCORE],
       'problem_pic': '/static/images/'+pic_name}


    return JsonResponse({'problem_info': dic})

@csrf_exempt
def submit_test_result(request):
    """
        后端应在此处保存这次答题的结果
        学生id从request.session获取
        时间数据、分数数据、试题名称见下面样例
        返回空Json即可
    """
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')
    print id
    print request.POST
    time_list = [int(item) for item in request.POST.get('time_list').split(",")]
    score_list = [int(item) for item in request.POST.get('score_list').split(",")]
    test_name = request.POST.get('test_name')
    account = stu.idToAccountStudent(str(id))
    tmp = (stu.getStudentAllDictByAccount(account))[Student.ESTIMATE_SCORE]
    if tmp.strip() == '':
        tmp = '{}'
    stu_dic = eval(tmp)
    stu_dic[test_name] = {'time': sum(time_list), 'score': sum(score_list)}
    stu.setStudent(account, Student.ESTIMATE_SCORE, str(stu_dic))
    return JsonResponse({})
