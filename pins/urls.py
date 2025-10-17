from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),             # home page
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('boards/create/', views.create_board, name='create_board'),
    path('boards/', views.board_list, name='board_list'),
    path('pins/create/', views.create_pin, name='create_pin'),

]
