#encoding=utf-8
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import  csrf_exempt

# Create your views here.

@ensure_csrf_cookie
def search_student(request):
	id = request.session.get('user_id', -1)
	if id == -1:
		return HttpResponse('Access denied')
	t = get_template('volunteer/v_list_student.html')
	c = {'id': id}
	return HttpResponse(t.render(c))

@csrf_exempt
def profile(request):
    print "heh333e"
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
        return render(request, 'v_userinfo.html',{'dict':dict})

