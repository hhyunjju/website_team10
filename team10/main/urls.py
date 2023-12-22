# main/urls.py
from django.urls import path
from . import views
####
app_name = 'main'
urlpatterns = [
    path('', views.indexcss, name='indexcss'),
    # path('chat', views.chat, name='chat'),
    path('byhtml/', views.test),
    path('policySvcMain/', views.get_policySvcMain, name='policySvc'),
    path('privateMain/', views.get_privateMain, name='private'),
    
    #display both cameras
    path('bycv2/', views.index, name='index'),

    #access the laptop camera
    path('bycv2/video_feed/', views.video_feed, name='video_feed'),

    #access the phone camera
    path('bycv2/webcam_feed/', views.webcam_feed, name='webcam_feed'),

]