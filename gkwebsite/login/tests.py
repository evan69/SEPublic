# encoding=utf-8
from django.test import TestCase
from django.test.client import Client
from django.test.utils import setup_test_environment
from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import redirect
import GenerateVerify

import sys

sys.path.append("../")
import database.teacher_backend as teacher_backend
import database.volunteer_backend as volunteer_backend

# Create your tests here.
setup_test_environment()
# test the login view
class LoginTest(TestCase):
    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
