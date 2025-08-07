from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    """Project model linked to a client."""
    
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        help_text=_('Name of the project')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Optional description of the project')
    )
    
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name=_('Client')
    )
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='created_projects',
        verbose_name=_('Created By')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['name']
        unique_together = ['name', 'client']
    
    def __str__(self):
        return f"{self.name} ({self.client.name})"


class LogSource(models.Model):
    """Log source configuration for SFTP and S3."""
    
    class SourceType(models.TextChoices):
        SFTP = 'sftp', _('SFTP')
        S3 = 's3', _('Amazon S3')
    
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='log_source',
        verbose_name=_('Project')
    )
    
    source_type = models.CharField(
        max_length=4,
        choices=SourceType.choices,
        default=SourceType.SFTP,
        verbose_name=_('Source Type')
    )
    
    # SFTP fields
    host = models.CharField(
        max_length=255,
        verbose_name=_('Host'),
        help_text=_('Server hostname or IP address'),
        blank=True
    )
    
    port = models.IntegerField(
        default=22,
        verbose_name=_('Port'),
        help_text=_('Server port (22 for SFTP)'),
        blank=True,
        null=True
    )
    
    username = models.CharField(
        max_length=255,
        verbose_name=_('Username'),
        blank=True
    )
    
    password = models.CharField(
        max_length=255,
        verbose_name=_('Password'),
        blank=True
    )
    
    directory = models.CharField(
        max_length=500,
        verbose_name=_('Directory'),
        help_text=_('Directory path where logs are located'),
        blank=True
    )
    
    # S3 fields
    bucket_name = models.CharField(
        max_length=255,
        verbose_name=_('Bucket Name'),
        help_text=_('S3 bucket name'),
        blank=True
    )
    
    region = models.CharField(
        max_length=50,
        verbose_name=_('Region'),
        help_text=_('AWS region (e.g., us-east-1)'),
        blank=True
    )
    
    access_key_id = models.CharField(
        max_length=255,
        verbose_name=_('Access Key ID'),
        help_text=_('AWS Access Key ID'),
        blank=True
    )
    
    secret_access_key = models.CharField(
        max_length=255,
        verbose_name=_('Secret Access Key'),
        help_text=_('AWS Secret Access Key'),
        blank=True
    )
    
    prefix = models.CharField(
        max_length=500,
        verbose_name=_('Prefix'),
        help_text=_('S3 object prefix/folder path'),
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Log Source')
        verbose_name_plural = _('Log Sources')
    
    def __str__(self):
        if self.source_type == self.SourceType.SFTP:
            return f"SFTP - {self.host}:{self.port}"
        else:
            return f"S3 - {self.bucket_name}/{self.prefix}"
    
    def clean(self):
        """Validate that required fields are filled based on source type."""
        from django.core.exceptions import ValidationError
        
        if self.source_type == self.SourceType.SFTP:
            if not self.host:
                raise ValidationError({'host': 'Host is required for SFTP sources.'})
            if not self.username:
                raise ValidationError({'username': 'Username is required for SFTP sources.'})
            if not self.directory:
                raise ValidationError({'directory': 'Directory is required for SFTP sources.'})
        elif self.source_type == self.SourceType.S3:
            if not self.bucket_name:
                raise ValidationError({'bucket_name': 'Bucket name is required for S3 sources.'})
            if not self.region:
                raise ValidationError({'region': 'Region is required for S3 sources.'})
            if not self.access_key_id:
                raise ValidationError({'access_key_id': 'Access Key ID is required for S3 sources.'})
            if not self.secret_access_key:
                raise ValidationError({'secret_access_key': 'Secret Access Key is required for S3 sources.'})


class FileFilter(models.Model):
    """File filtering configuration for log files."""
    
    class FilterType(models.TextChoices):
        STARTS_WITH = 'starts_with', _('Starts With')
        CONTAINS = 'contains', _('Contains')
        REGEX = 'regex', _('Regex Match')
    
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='file_filter',
        verbose_name=_('Project')
    )
    
    filter_type = models.CharField(
        max_length=11,
        choices=FilterType.choices,
        default=FilterType.STARTS_WITH,
        verbose_name=_('Filter Type')
    )
    
    pattern = models.CharField(
        max_length=255,
        verbose_name=_('Pattern'),
        help_text=_('Pattern to match files (filename pattern, regex, etc.)')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('File Filter')
        verbose_name_plural = _('File Filters')
    
    def __str__(self):
        return f"{self.get_filter_type_display()}: {self.pattern}"


class Schedule(models.Model):
    """Cron-based scheduling configuration."""
    
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='schedule',
        verbose_name=_('Project')
    )
    
    cron_expression = models.CharField(
        max_length=100,
        verbose_name=_('Cron Expression'),
        help_text=_('Cron expression (e.g., "0 */6 * * *" for every 6 hours)')
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active'),
        help_text=_('Whether this schedule is active')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')
    
    def __str__(self):
        return f"{self.project.name} - {self.cron_expression}"
