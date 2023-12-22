from django.contrib import admin
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),  # 로그인 URL 설정
    path('register/', views.register_view, name='register'),  # 회원가입 URL 설정
    # 추가적인 URL 설정을 필요에 따라 작성하세요.
]