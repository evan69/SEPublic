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
	# for debug here
	id = request.session.get('user_id', -1)
	if id == -1:
		return HttpResponse('Access denied')
	t = get_template('volunteer/v_list_student.html')
	c = {'id': id}
	return HttpResponse(t.render(c))

def student_list_all(request):
	print request.session.get('user_id')
	'''
		后端需要在这里改代码，根据志愿者id返回这个志愿者可以见到的学生列表信息
		后端可以通过request.session.get('user_id')获取id
	'''
	if request.is_ajax() and request.method == 'POST':
		t = []
		c = {'id':'151099','name':'王二', 'gender':'男', 'source':'北京', 'school':'人大附中', 'id_card':'11010819980824181X'}
		# SELECT * FROM student
		t = []
		t.append(c)
		d = {'id':'151016','name':'张三', 'gender':'男', 'source':'湖北', 'school':'黄冈中学', 'id_card':'520108199808241894'}
		t.append(d)
		e = {'id':'152357','name':'李四', 'gender':'女', 'source':'湖北', 'school':'黄冈中学', 'id_card':'520108199808241864'}
		t.append(e)
		f = {'id':'159930','name':'阿不来提·阿卜杜热西提', 'gender':'男', 'source':'新疆', 'school':'乌鲁木齐市第一中学', 'id_card':'86010819980824187X'}
		t.append(f)
		return JsonResponse(t, safe=False)	# must use 'safe=False'
	else:
		return HttpResponse('Access denied.')

def student_info_show(request):
    t = get_template('volunteer/student_info.html')
    c = Context({})
    print request.session.get('user_id')
    return HttpResponse(t.render(c))

def dashboard(request):
	return HttpResponse('YES')
@csrf_exempt
def profile(request):
    print "heh333e"
    if request.method == 'POST':
        '''
        	后端需要在这里改代码，保存传进来的数据到数据库，并返回正确的dict。
        	希望能够返回是否保存成功，以及哪些字段不合法的信息
        	后端可以通过request.session.get('user_id')获取id
        '''
        print request.POST
        volunteer_name = request.POST.get('volunteer_name', 'byr')
        phone = request.POST.get('phone', '110')
        dict = {'volunteer_name': '李三胖', 'email': '1@q.com', 'work_address': '2', 'home_address': '10', 'postcode': '3',
                'homephone': '4', 'phone': phone, 'qqn': '5', 'weichat': '6', 'describe': '7', }
        return JsonResponse(dict)
    else:
        '''
            后端需要在这里改代码，从数据库读取正确的dict，并返回
        '''
        dict = {'volunteer_name': '百叫猿', 'email': '11', 'work_address': '22', 'home_address': '130', 'postcode': '43',
                'homephone': '49', 'phone': '666', 'qqn': '85', 'weichat': '66', 'describe': '57', }
        return render(request, 'v_userinfo.html',{'dict':dict})

