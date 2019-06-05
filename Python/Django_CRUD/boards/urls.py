from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new/', views.new),  # 사용자 입력 페이지
    path('create/', views.create),  # 데이터 저장 페이지
]