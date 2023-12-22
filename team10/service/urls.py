from django.urls import path
from . import views

app_name = 'service'  # 앱 이름 설정

urlpatterns = [
    path('', views.index, name='service'),  # 기본 URL 패턴 (나중에 변경 가능)
]