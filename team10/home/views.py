# home/views.py

from django.shortcuts import render

def home_view(request):
    # 필요한 로직
    return render(request, 'home/home.html')


def intro(request):
    return render(request, 'home/intro.html')

