# admin.py
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Post, Page, Series, Category, Comment, SeriesPost
from django.contrib import messages

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created', 'published_date')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('status', 'categories')
    search_fields = ('title', 'content')


@admin.register(Page)
class PageAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ['title', 'display_order', 'keyword', 'order', 'main_menu']
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('created',)
    search_fields = ('title', 'content')

    @admin.display(description="Order")
    def display_order(self, obj):
        return obj.order


@admin.register(SeriesPost)
class SeriesPostAdmin(SortableAdminMixin, admin.ModelAdmin):  # type: ignore[misc]
    list_display = ('series', 'post', 'display_order', 'order')
    list_filter = ('post', 'series')
    search_fields = ('post',)

    @admin.display(description="Order")
    def display_order(self, obj):
        return obj.order


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'status', 'slug']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ("name", "slug", "parent")
    prepopulated_fields = {"slug": ("name",)}


@admin.action(description="Approve selected comments")
def approve_comments(modeladmin, request, queryset):
    updated = queryset.update(active=True)

    modeladmin.message_user(
        request,
        f"{updated} comments approved.",
        messages.SUCCESS,
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "parent", "created", "active")
    list_filter = ("post", "user")
    search_fields = ("content",)
    actions = [approve_comments]
