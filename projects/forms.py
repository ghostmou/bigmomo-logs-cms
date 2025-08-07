from django import forms
from .models import Project, LogSource, FileFilter, Schedule


class ProjectForm(forms.ModelForm):
    """Form for creating and updating projects."""
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'client']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter project description'}),
            'client': forms.Select(attrs={'class': 'form-control'})
        }


class LogSourceForm(forms.ModelForm):
    """Form for configuring log sources."""
    
    class Meta:
        model = LogSource
        fields = ['source_type', 'host', 'port', 'username', 'password', 'directory']
        widgets = {
            'source_type': forms.Select(attrs={'class': 'form-control'}),
            'host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., ftp.example.com'}),
            'port': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 65535}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'directory': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/path/to/logs'})
        }


class FileFilterForm(forms.ModelForm):
    """Form for configuring file filters."""
    
    class Meta:
        model = FileFilter
        fields = ['filter_type', 'pattern']
        widgets = {
            'filter_type': forms.Select(attrs={'class': 'form-control'}),
            'pattern': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter filter pattern'})
        }


class ScheduleForm(forms.ModelForm):
    """Form for configuring schedules."""
    
    class Meta:
        model = Schedule
        fields = ['cron_expression', 'is_active']
        widgets = {
            'cron_expression': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 0 */6 * * *'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        help_texts = {
            'cron_expression': 'Cron expression format: minute hour day month day_of_week'
        }
