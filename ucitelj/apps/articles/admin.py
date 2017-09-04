from django.contrib import admin
from .models import Article, ArticleText


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article)
admin.site.register(ArticleText)
