from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import *

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),  # 로그인 URL 설정
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # 회원가입 URL 설정
    path('signup/', views.signup, name='signup'),
    path("profile", views.profile, name='profile'),
    path("password_change/", auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done')),
         name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    
]