#encoding=utf-8
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.http import HttpResponse, request
from django.template import RequestContext
from django.template.loader import get_template
from django.template import Context
# Create your views here.
from django.views.decorators.csrf import csrf_protect, csrf_exempt


def search_student(request):
    t = get_template('teacher/list_student.html')
    c = Context({})
    return HttpResponse(t.render(c))


'''
    查看和修改教师个人信息
    by byr 161012
'''
#@csrf_protect
@csrf_exempt
def profile(request):
    if request.method == 'POST':
        print "heheda"
        teacher_name = request.POST.get('teacher_name', 'byr')
        phone = request.POST.get('phone', '110')
        dict = {'teacher_name': teacher_name, 'email': '1', 'work_address': '2', 'home_address': '10', 'postcode': '3',
                'homephone': '4', 'phone': phone, 'qqn': '5', 'weichat': '6', 'describe': '7', }
        return JsonResponse(dict)
    else:
        return render_to_response('userinfo.html',context_instance=RequestContext(request))
