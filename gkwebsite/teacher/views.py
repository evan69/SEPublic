#encoding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@ensure_csrf_cookie
def search_student(request):
	id = request.session.get('user_id', -1)
	if id == -1:
		return HttpResponse('Access denied')
	t = get_template('teacher/list_student.html')
	c = {'id':id}
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
        			后端需要在这里改代码，返回正确的dict
        '''
        teacher_name = request.POST.get('teacher_name', 'byr')
        phone = request.POST.get('phone', '110')
        dict = {'teacher_name': teacher_name, 'email': '1', 'work_address': '2', 'home_address': '10', 'postcode': '3',
                'homephone': '4', 'phone': phone, 'qqn': '5', 'weichat': '6', 'describe': '7', }
        return JsonResponse(dict)
    else:
        return render_to_response('userinfo.html',context_instance=RequestContext(request))

