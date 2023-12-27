from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.conf import settings
from .models import Profile
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
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

class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        messages.info(self.request, '비밀번호 변경이 완료되었습니다')
        return super().form_valid(form)
    
def cookie_test(request, code):
    response = render(request, 'registration/cookieTest.html')
    if code == 'add': # Set-Cookie 헤더를 보내어 브라우저에 쿠키를 생성하도록 지시
        response.set_cookie('model', 'A001') # 'model' 쿠키에는 'A001', 
        response.set_cookie('prod', 'EV9') # 'prod' 쿠키에는 'EV9'라는 값이 설정
    elif code == 'get': #조회
        model = request.COOKIES.get('model')
        prod = request.COOKIES.get('prod')
        print(model, prod)
    elif code == 'del':
        response.delete_cookie('model')
        response.delete_cookie('prod')
    return response
