from django.shortcuts import render
from django.http import HttpResponse, request
from django.template.loader import get_template
from django.template import Context

from django.shortcuts import redirect

# Create your views here.

def search_student(request):
	t = get_template('teacher/list_student.html')
	c = Context({})
	return HttpResponse(t.render(c))

def student_info_edit(request):
	t = get_template('teacher/student_info_edit.html')
	c = Context({})
	return  HttpResponse(t.render(c))


def student_info_save(request):
	t = get_template('techer/student_info.html')
	c = Context({})
	return HttpResponse(t.render(c))

def student_info_show(request):
	t = get_template('teacher/student_info.html')
	c = Context({})
	return HttpResponse(t.render(c))
