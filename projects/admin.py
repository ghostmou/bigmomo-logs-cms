from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Project, LogSource, FileFilter, Schedule


class LogSourceInline(admin.StackedInline):
    model = LogSource
    extra = 0
    fields = ['source_type', 'host', 'port', 'username', 'password', 'directory']


class FileFilterInline(admin.StackedInline):
    model = FileFilter
    extra = 0
    fields = ['filter_type', 'pattern']


class ScheduleInline(admin.StackedInline):
    model = Schedule
    extra = 0
    fields = ['cron_expression', 'is_active']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for Project model."""
    
    list_display = ['name', 'client', 'created_by', 'has_log_source', 'has_file_filter', 'has_schedule', 'created_at']
    list_filter = ['client', 'created_at']
    search_fields = ['name', 'client__name', 'created_by__username']
    ordering = ['name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'client', 'created_by')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [LogSourceInline, FileFilterInline, ScheduleInline]
    readonly_fields = ['created_at', 'updated_at']
    
    def has_log_source(self, obj):
        return hasattr(obj, 'log_source')
    has_log_source.boolean = True
    has_log_source.short_description = 'Log Source'
    
    def has_file_filter(self, obj):
        return hasattr(obj, 'file_filter')
    has_file_filter.boolean = True
    has_file_filter.short_description = 'File Filter'
    
    def has_schedule(self, obj):
        return hasattr(obj, 'schedule')
    has_schedule.boolean = True
    has_schedule.short_description = 'Schedule'


@admin.register(LogSource)
class LogSourceAdmin(admin.ModelAdmin):
    """Admin interface for LogSource model."""
    
    list_display = ['project', 'source_type', 'host', 'port', 'username', 'created_at']
    list_filter = ['source_type', 'created_at']
    search_fields = ['project__name', 'host', 'username']
    ordering = ['project__name']


@admin.register(FileFilter)
class FileFilterAdmin(admin.ModelAdmin):
    """Admin interface for FileFilter model."""
    
    list_display = ['project', 'filter_type', 'pattern', 'created_at']
    list_filter = ['filter_type', 'created_at']
    search_fields = ['project__name', 'pattern']
    ordering = ['project__name']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Admin interface for Schedule model."""
    
    list_display = ['project', 'cron_expression', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['project__name', 'cron_expression']
    ordering = ['project__name']
