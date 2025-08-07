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
        fields = [
            'source_type', 'host', 'port', 'username', 'password', 'directory',
            'bucket_name', 'region', 'access_key_id', 'secret_access_key', 'prefix'
        ]
        widgets = {
            'source_type': forms.Select(attrs={'class': 'form-control'}),
            'host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., sftp.example.com'}),
            'port': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 65535}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'directory': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/path/to/logs'}),
            'bucket_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., my-logs-bucket'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., us-east-1'}),
            'access_key_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AWS Access Key ID'}),
            'secret_access_key': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'AWS Secret Access Key'}),
            'prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., logs/2024/'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for conditional display
        if self.instance and self.instance.pk:
            self.fields['source_type'].initial = self.instance.source_type
        else:
            self.fields['source_type'].initial = 'sftp'
    
    def clean(self):
        """Validate that required fields are filled based on source type."""
        cleaned_data = super().clean()
        source_type = cleaned_data.get('source_type')
        
        if source_type == 'sftp':
            # Validate SFTP required fields
            if not cleaned_data.get('host'):
                self.add_error('host', 'Host is required for SFTP sources.')
            if not cleaned_data.get('username'):
                self.add_error('username', 'Username is required for SFTP sources.')
            if not cleaned_data.get('directory'):
                self.add_error('directory', 'Directory is required for SFTP sources.')
        elif source_type == 's3':
            # Validate S3 required fields
            if not cleaned_data.get('bucket_name'):
                self.add_error('bucket_name', 'Bucket name is required for S3 sources.')
            if not cleaned_data.get('region'):
                self.add_error('region', 'Region is required for S3 sources.')
            if not cleaned_data.get('access_key_id'):
                self.add_error('access_key_id', 'Access Key ID is required for S3 sources.')
            if not cleaned_data.get('secret_access_key'):
                self.add_error('secret_access_key', 'Secret Access Key is required for S3 sources.')
        
        return cleaned_data


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
