from django.urls import path
from . import views

app_name = 'brd'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:no>/', views.detail, name='detail'),
    path('update/<id>/', views.post_update , name='update'),
    path('delete/<id>/', views.post_delete , name='delete'), 
    path('notice_board/', views.notice_board_view, name='notice_board'),
    path('faq/', views.faq_view, name='faq'),
]