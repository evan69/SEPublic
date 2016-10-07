from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import datetime

# Create your views here.

def student_center(request):
	t = get_template('student/center.html')
	c = Context({'id': 2014011425})
	#request.session['user_id'] = 2014011425
	return HttpResponse(t.render(c))
	
def student_score(request):
	t = get_template('student/score.html')
	id = request.session.get('user_id', -1)
	if id == -1:
		return HttpResponse('Access denied')
	c = Context({'id': id})
	return HttpResponse(t.render(c))
	
def student_rank(request):
	return HttpResponse('This is RANK page.')
	
def student_admit(request):
	return HttpResponse('This is ADMIT page.')
	
def student_contact(request):
	return HttpResponse('This is CONTACT page.')