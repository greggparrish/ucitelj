from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('subscriptions/', views.subscription),
    path('<slug>/', views.detail),
]
