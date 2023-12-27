# home/urls.py

from django.urls import path
from . import views
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('intro/', views.intro, name='intro'),
]
