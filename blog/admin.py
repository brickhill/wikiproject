# admin.py
from django.contrib import admin
from .models import Post, Page, Series, Category, Comment, SeriesPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created', 'published_date')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('status', 'categories', 'series')
    search_fields = ('title', 'content')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'keyword')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('created',)
    search_fields = ('title', 'content')

@admin.register(SeriesPost)
class SeriesPostAdmin(admin.ModelAdmin):
    list_display = ('series', 'post', 'priority')
    list_filter = ('post',)
    search_fields = ('post',)

admin.site.register(Series)
admin.site.register(Category)
admin.site.register(Comment)
