from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.conf import settings
from .models import Profile
from django.contrib import messages
# 회원가입 뷰 작성

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form':form})

def profile(request):
    profile = get_object_or_404(Profile, user=request.user )
    return render(request, 'registration/profile.html', {'profile':profile})

