# admin.py
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Post, Page, Series, Category, Comment, SeriesPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created', 'published_date')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('status', 'categories')
    search_fields = ('title', 'content')


@admin.register(Page)
class PageAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    # TODO Draggable doesn't update the page on dragging.
    list_display = ['title', 'display_order', 'keyword', 'order']
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('created',)
    search_fields = ('title', 'content')
    @admin.display(description="Order")
    def display_order(self, obj):
        return obj.order

@admin.register(SeriesPost)
class SeriesPostAdmin(SortableAdminMixin,admin.ModelAdmin): # type: ignore[misc]
    list_display = ('series', 'post', 'display_order', 'order')
    list_filter = ('post', 'series')
    search_fields = ('post',)
    @admin.display(description="Order")
    def display_order(self, obj):
        return obj.order

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

  
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Comment)
