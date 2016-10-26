# encoding=utf-8
from django.http import JsonResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import redirect
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

import GenerateVerify

import sys

sys.path.append("../")
import database.teacher_backend as teacher_backend
import database.volunteer_backend as volunteer_backend

'''
    login & register 界面
    by byr 161003
'''

@csrf_exempt
def login(request):
    return render(request, 'src/login.html')


'''
    login 表单检查
    by byr 161006
'''
@csrf_exempt
def logincheck(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('login_username', ''):
            errors.append('enter login username')
        if not request.POST.get('login_password', ''):
            errors.append('enter login password')
        if not request.POST.get('login_yzm', ''):
            errors.append('enter login yzm')
        if not errors:
            if 'student' in request.POST:
                username = request.POST.get('login_username')
                password = request.POST.get('login_password')
                request.session['user_id'] = 10086
                request.session['user_name'] = username
                request.session['password'] = password
                # return render_to_response('/student')
                return redirect('/student')
            elif 'teacher' in request.POST:
                username = request.POST.get('login_username')
                password = request.POST.get('login_password')
                yzmString = request.POST.get('login_yzm').upper()
                if (yzmString == request.session['yzmString']):
                    print ' teacher login'
                    (login,id) = teacher_backend.checkTeacherPassword(username, password)
                    if login:
                        request.session['user_id'] = int(id)
                        request.session['user_name'] = username
                        request.session['password'] = password
                        return redirect('/teacher/')
                    else:
                        return HttpResponse(u"教师界面登录失败")
                else:
                    return HttpResponse(u"教师界面登录失败")
            elif 'volunteer' in request.POST:
                username = request.POST.get('login_username')
                password = request.POST.get('login_password')
                yzmString = request.POST.get('login_yzm').upper()
                if (yzmString == request.session['yzmString']):
                    (login,id) = volunteer_backend.checkVolunteerPassword(username, password)
                    if login:
                        request.session['user_id'] = id
                        request.session['user_name'] = username
                        request.session['password'] = password
                        # return render_to_response('/student')
                        return redirect('/volunteer')
                        #return HttpResponse(u"志愿者界面")
                    else:
                        return HttpResponse(u"志愿者界面登录失败")
                else:
                    return HttpResponse(u'验证码不正确')
            else:
                return render_to_response('src/login.html');
    else:
        return render_to_response('src/login.html', {'errors': errors});


'''
    登录界面验证码生成
    by byr 161009
'''
def gnrtyzm(request, width, height):
    img, yzmString = GenerateVerify.gnrtyzm(width, height)
    request.session['yzmString'] = yzmString
    return HttpResponse(img, 'image/jpeg')

'''
    发送邮件功能
    by byr 161026
'''
def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr(( \
		Header(name, 'utf-8').encode(), \
		addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def sendEmail(toEmail):
    from_addr = 'bbwrld@sina.com'
    password = 'bibiworld'
    to_addr = toEmail
    smtp_server = 'smtp.sina.com'
    msg = MIMEText('清华欢迎你\n欢迎报考清华大学！\n', 'plain', 'utf-8')
    msg['From'] = _format_addr(u'BIBIGroup <%s>' % from_addr)
    msg['To'] = _format_addr(u'亲 <%s>' % to_addr)
    msg['Subject'] = Header(u'来自早起早睡小组的问候', 'utf-8')
    '''
    	如果MIMEText()中不含中文, subject有中文, 则无法发送邮件
    	如果都不含中文, 可以发送邮件; 如果都含中文, 也可以发送邮件
    '''
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


'''
    注册功能
    by byr 161026
'''
@csrf_protect
def register(request):
    '''
    后端需要检验邀请码和相关信息
    无误后写入到数据库
    '''
    username = request.POST.get('username', '1')
    password = request.POST.get('password','2')
    email = request.POST.get('email','3')
    invited = request.POST.get('invited','4')


    print email
    success = True
    if (success):
        sendEmail(email)


    return JsonResponse({'result': '注册成功'})





