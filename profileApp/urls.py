from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_profile, name='my_profile'),  # ✅ for /profile/
    path('edit/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.view_profile, name='view_profile'),
]
