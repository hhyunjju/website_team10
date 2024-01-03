from django.urls import path
from . import views


app_name = 'service'  # 앱 이름 설정

urlpatterns = [
    #path('', views.index, name='service'), 
    path('model/', views.model, name='model'),
    path('service/', views.service, name='service'),
    path('statistics/', views.statistics, name='statistics'),
    path('test/', views.test, name='test'),
    path('send_image/', views.send_image, name='send_image'),
]