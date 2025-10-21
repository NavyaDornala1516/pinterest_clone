from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_home(request):
    return redirect('home')

urlpatterns = [
    path('', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('boards/create/', views.create_board, name='create_board'),
    path('boards/', views.board_list, name='board_list'),
    path('pins/create/', views.create_pin, name='create_pin'),
    path('delete/<int:pk>/', views.delete_pin, name='delete_pin'),
]
