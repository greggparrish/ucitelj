from django.contrib import admin
from .models import Article, ArticleText


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('date', 'feed', 'title')
    list_filter = ('feed',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleText)
