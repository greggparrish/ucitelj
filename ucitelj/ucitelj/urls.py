from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html")),
    path('admin/', admin.site.urls),

    path('articles/', include('apps.articles.urls')),
    path('feeds/', include('apps.feeds.urls')),
    path('users/', include('apps.users.urls')),
    path('words/', include('apps.words.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
