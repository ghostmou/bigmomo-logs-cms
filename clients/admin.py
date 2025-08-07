from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin interface for Client model."""
    
    list_display = ['name', 'created_by', 'project_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'created_by__username']
    ordering = ['name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'created_by')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def project_count(self, obj):
        return obj.get_project_count()
    project_count.short_description = 'Projects'
