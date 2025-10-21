from django.urls import path
from . import views

urlpatterns = [
    path('', views.boards_list, name='boards_list'),  
    path('create/', views.create_board, name='create_board'),
]
