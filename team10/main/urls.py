from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('byhtml/', views.test),
    path('policySvcMain/', views.get_policySvcMain),
    path('privateMain/', views.get_privateMain),
    
    #display both cameras
    path('bycv2/', views.index, name='index'),

    #access the laptop camera
    path('video_feed/', views.video_feed, name='video_feed'),

    #access the phone camera
    path('webcam_feed/', views.webcam_feed, name='webcam_feed'),

]