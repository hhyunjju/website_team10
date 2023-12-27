# home/views.py

from django.shortcuts import render

def home_view(request):
    return render(request, 'layout.html')

def home(request):
    return render(request, 'home/home.html')


def intro(request):
    return render(request, 'home/intro.html')