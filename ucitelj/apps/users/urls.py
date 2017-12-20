from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('register/', views.register),
]
