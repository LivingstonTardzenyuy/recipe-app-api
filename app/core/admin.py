from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _ 

class UserAdmin(BaseUserAdmin):
    # Specify which fields to display in the admin
    list_display = ('email', 'name', 'nickname', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'nickname')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2', 'name', 'nickname', 'is_active', 'is_staff')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Register the custom User model and UserAdmin
admin.site.register(User, UserAdmin)
