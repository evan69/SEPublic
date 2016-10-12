# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, request, JsonResponse
from django.template.loader import get_template
from django.template import Context

from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.

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