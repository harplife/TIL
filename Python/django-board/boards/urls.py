from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('<int:board_id>/detail/', views.detail, name='detail'),
    path('delete/<int:board_id>/', views.delete, name='delete'),
    path('edit/<int:board_id>/', views.edit, name='edit'),

    # Comments
    path('<int:board_id>/new_comment/', views.new_comment, name='new_comment'),
    path('<int:board_id>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
