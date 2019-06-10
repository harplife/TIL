from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('new/', views.new),
    path('create/', views.create),
    path('<int:id>/', views.detail),
    path('delete/<int:id>/', views.delete),
]