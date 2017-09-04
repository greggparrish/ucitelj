from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^subscriptions/', views.subscription, name='subscription'),
    url(r'^(?P<slug>[\w-]+)/$', views.detail, name='detail'),
]
