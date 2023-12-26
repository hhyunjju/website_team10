# service/views.py

from django.shortcuts import render
from django.http import HttpResponse


#임시로 만들었습니다
def model(request):
    return render(request, 'service/model.html')
def service(request):
    return render(request, 'service/service.html')
def statistics(request):
    return render(request, 'service/statistics.html')