from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for custom User model."""
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'status', 'is_password_changed', 'date_joined']
    list_filter = ['role', 'status', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Password Info'), {'fields': ('is_password_changed',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'status'),
        }),
    )
    
    readonly_fields = ['is_password_changed', 'date_joined', 'last_login']
    
    def get_queryset(self, request):
        """Prevent users from blocking themselves."""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs
        return qs
    
    def save_model(self, request, obj, form, change):
        """Set password changed flag when password is changed."""
        if change and 'password' in form.changed_data:
            obj.is_password_changed = True
        super().save_model(request, obj, form, change)
