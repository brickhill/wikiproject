# admin.py
from django.contrib import admin
from .models import Post, Page, Series, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('status', 'categories', 'series')
    search_fields = ('title', 'content')

admin.site.register(Page)
admin.site.register(Series)
admin.site.register(Category)