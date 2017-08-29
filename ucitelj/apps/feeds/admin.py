from django.contrib import admin
from .models import Feed

class FeedAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Feed, FeedAdmin)
