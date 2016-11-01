#encoding=utf-8
from django.http import JsonResponse
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
import database.teacher_backend as tch
import database.backend as back


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
    '''

    后端需要获取录取信息传给前端
    '''
    id = request.session.get('user_id', -1)
    if id == -1:
        return HttpResponse('Access denied')


    student_dic = stu.getStudentAllDictByAccount(stu.idToAccountStudent(str(id)))
    info = student_dic[Student.ADMISSION_STATUS]
    if info.strip() == '' or info.strip() == "0":
        info = u'暂时还没有您的录取信息，请耐心等待老师添加'
    admition = info
    return render(request,
                  'student/admit.html', {'admition': admition})


def student_contact(request):
    '''
                后端需要在这里改代码，从数据库读取正确的dict，并返回
    '''
    teacher_list = tch.getAllInTeacher()
    list = []
    for teacher in teacher_list:
        account = getattr(teacher, Teacher.ACCOUNT)
        name = tch.getTeacher(account, Teacher.REAL_NAME)
        phone = tch.getTeacher(account, Teacher.PHONE)
        email = tch.getTeacher(account, Teacher.EMAIL)
        address = tch.getTeacher(account, Teacher.AREA)
        dict = {'name':name, 'phone':phone,'email':email,'address':address}
        list.append(dict)
    return render(request,'student/contact.html', {'dict': list})


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
        'estimateScore': 'estimateScore',
        'estimateRank': 'estimateRank',
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
        id = request.session.get('user_id', -1)
        if id == -1:
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
                dic['group' + str(i)] = group_list[i]
            else:
                dic['group' + str(i)] = '0'

        dic['grouplist'] = [' ']
        all_group = back.getGroupbyDict({})
        for item in all_group:
            dic['grouplist'].append(back.getGroupAllDictByObject(item)['id'])
        print request.POST
        return render(request, 'student/userinfo.html', {'dict': dict})

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



