#encoding=utf-8
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import  csrf_exempt




@ensure_csrf_cookie
def search_student(request):
	id = request.session.get('user_id', -1)
	if id == -1:
		return HttpResponse('Access denied')
	t = get_template('teacher/list_student.html')
	c = {'id': id}
	return HttpResponse(t.render(c))

def student_info_edit(request):
	t = get_template('teacher/student_info_edit.html')
	c = Context({})
	return  HttpResponse(t.render(c))


def student_info_save(request):
	t = get_template('teacher/student_info.html')
	c = Context({})
	return HttpResponse(t.render(c))

def student_info_show(request):
	t = get_template('teacher/student_info.html')
	c = Context({})
	return HttpResponse(t.render(c))

def add_student(request):
	id = request.session.get('user_id', -1)
	if id == -1:
		return HttpResponse('Access denied')
	#t = get_template('teacher/list_student.html')
	#c = {}
	#return HttpResponse(t.render(c))
	return HttpResponse('Add student page.')

def fake_backend(request):
	if request.is_ajax() and request.method == 'POST':
		c = {'name':'Alice', 'gender':'男', 'source':'北京', 'school':'人大附中', 'id_card':'11010819980824181X'}
		c['name']=request.POST.get('name')
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

'''
    查看和修改教师个人信息
    by byr 161012
'''
#@csrf_protect
@csrf_exempt
def profile(request):
    if request.method == 'POST':
        '''
        	后端需要在这里改代码，保存传进来的数据到数据库，并返回正确的dict
        '''
        teacher_name = request.POST.get('teacher_name', 'byr')
        phone = request.POST.get('phone', '110')
        dict = {'teacher_name': teacher_name, 'email': '1', 'work_address': '2', 'home_address': '10', 'postcode': '3',
                'homephone': '4', 'phone': phone, 'qqn': '5', 'weichat': '6', 'describe': '7', }
        return JsonResponse(dict)
    else:
        '''
            后端需要在这里改代码，从数据库读取正确的dict，并返回
        '''
        dict = {'teacher_name': '骚猴', 'email': '11', 'work_address': '22', 'home_address': '130', 'postcode': '43',
                'homephone': '49', 'phone': '666', 'qqn': '85', 'weichat': '66', 'describe': '57', }
        return render(request, 'teacher/userinfo.html',{'dict':dict})

'''
    老师上传试题
    by byr 161016
'''
@csrf_exempt
def upload(request):
	return render(request, 'teacher/uploadtest.html')

'''
    老师查看志愿者详情
    by byr 161017
'''
@csrf_exempt
def volunteer_info(request):
	'''
	后端需要在这里获取数据并返回
	'''

	dict = {
		'id' : 'heheda',
		'user_name' : 'lihy96',
		'realName' : '李三胖',
		'idNumber' : '1234567890X',
		'sex' : '女',
		'nation' : '内蒙古族',
		'birth_year' : '1996',
		'birth_month' : '01',
		'birth_date' : '01',
		'department' : '计算机系',
		'class' : '计45',
		'phone' : '123456789',
		'email' : 'lihy14@mails.tsinghua.edu.cn',
		'province' : '内蒙古',
		'distribute' : '1 | 2 | 3',
		'qqn' : '123456789',
		'weichat' : 'fdafs1231',
		'teacher' : '白老师 | 李老师',
		'comment' : '大家好，我叫李昊阳，人长得帅，还长得长，更有钱，很会跳街舞',
	}
	return render(request, 'teacher/volunteer_info.html', {'dict':dict})

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

		phone = request.POST.get('phone', '110')
		email = request.POST.get('email', '110@qq')
		dict = {
			'user_name': 'lihy96',
			'realName': '李三胖',
			'idNumber': '1234567890X',
			'sex': '女',
			'nation': '内蒙古族',
			'birth_year': '1996',
			'birth_month': '01',
			'birth_date': '01',
			'department': '计算机系',
			'class': '计45',
			'phone': phone,
			'email': email,
			'province': '内蒙古',
			'distribute': '1 | 2 | 3',
			'qqn': '123456789',
			'weichat': 'fdafs1231',
			'teacher': '白老师 | 李老师',
			'comment': '大家好，我叫李昊阳，人长得帅，还长得长，更有钱，很会跳街舞',
		}
		return JsonResponse(dict)
	else:
		'''
            后端需要在这里改代码，从数据库读取正确的dict，并返回
        '''
		user_id = request.GET.get('id', 'gou')

		dict = {
			'user_name': user_id,
			'realName': '李三胖',
			'idNumber': '1234567890X',
			'sex': '女',
			'nation': '内蒙古族',
			'birth_year': '1996',
			'birth_month': '01',
			'birth_date': '01',
			'department': '计算机系',
			'class': '计45',
			'phone': '123456789',
			'email': 'lihy14@mails.tsinghua.edu.cn',
			'province': '内蒙古',
			'distribute': '1 | 2 | 3',
			'qqn': '123456789',
			'weichat': 'fdafs1231',
			'teacher': '白老师 | 李老师',
			'comment': '大家好，我叫李昊阳，人长得帅，还长得长，更有钱，很会跳街舞',
		}
		return render(request, 'teacher/volunteer_info_edit.html', {'dict': dict})


'''
    老师给学生分组
    by byr 161017
'''
def distribute_student(request):
	return render(request, 'teacher/distribute_student.html')