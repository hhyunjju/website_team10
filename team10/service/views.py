# service/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CameraImage


#임시로 만들었습니다
def model(request):
    return render(request, 'service/model.html')
def service(request):
    return render(request, 'service/service.html')
def statistics(request):
    return render(request, 'service/statistics.html')


def test(request):
    return render(request, 'service/test.html')

def test2(request):
    if request.method == 'POST':
        image = request.FILES.get('camera-image')
        CameraImage.objects.create(image=image)
    images = CameraImage.objects.all()
    context = {
        'images':images
    }
    return render(request, 'service/service.html', context)

def upload(request):
    if request.method == 'POST' and request.FILES['files']:
        image = request.FILES.get('camera-image')
        CameraImage.objects.create(image=image)
    images = CameraImage.objects.all()
    context = {
        'images':images
    }
    return render(request, 'service/service.html', context)

from django.http import JsonResponse
from .forms import ImageUploadForm
import numpy as np

num = 0


def send_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('img_file')
        img_dict = {'img':image_file}
        return render(request, 'service/success.html', context=img_dict)
    
def success(request):
    return render(request, 'service/success.html')