# admin.py PG
from django.contrib import admin
# from adminsortable2.admin import SortableAdminMixin
from .models import Organisation, Membership

# from django.contrib import messages

@admin.register(Organisation)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')
    search_fields = ('name',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('organisation', 'user', 'role')
    search_fields = ('organisation', 'user', 'role')