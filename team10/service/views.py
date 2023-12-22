# service/views.py

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Service 앱의 기본 페이지입니다.")