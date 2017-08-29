from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView



urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="home.html")),

    url(r'^admin/', admin.site.urls),

    url(r'^/', include('apps.feeds.urls')),

    url(r'^articles/', include('apps.feeds.urls')),
    url(r'^feeds/', include('apps.feeds.urls')),
    url(r'^words/', include('apps.feeds.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
