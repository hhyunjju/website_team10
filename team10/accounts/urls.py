from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import *

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),  # 로그인 URL 설정
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # 회원가입 URL 설정
    path('signup/', views.signup, name='signup'),
    path("profile", views.profile, name='profile'),

]