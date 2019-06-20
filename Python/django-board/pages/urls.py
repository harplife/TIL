from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/update/', views.update, name='update'),

    # comments
    # POST /boards/3/comments/
    path('<int:post_pk>/comment/', views.make_comment, name='make_comment'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),

    # like
    path('<int:post_pk>/like/', views.like, name='like'),

    # follow
    path('<int:post_pk>/follow/<int:user_pk>/', views.follow, name='follow'),
]
