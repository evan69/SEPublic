#encoding=utf-8
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context

from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token
from django.views.decorators.csrf import  csrf_exempt




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
        return render(request, 'userinfo.html',{'dict':dict})

