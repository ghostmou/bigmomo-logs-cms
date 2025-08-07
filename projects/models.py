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
    """Log source configuration for FTP/SFTP."""
    
    class SourceType(models.TextChoices):
        FTP = 'ftp', _('FTP')
        SFTP = 'sftp', _('SFTP')
    
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
    
    host = models.CharField(
        max_length=255,
        verbose_name=_('Host'),
        help_text=_('Server hostname or IP address')
    )
    
    port = models.IntegerField(
        default=22,
        verbose_name=_('Port'),
        help_text=_('Server port (22 for SFTP, 21 for FTP)')
    )
    
    username = models.CharField(
        max_length=255,
        verbose_name=_('Username')
    )
    
    password = models.CharField(
        max_length=255,
        verbose_name=_('Password')
    )
    
    directory = models.CharField(
        max_length=500,
        verbose_name=_('Directory'),
        help_text=_('Directory path where logs are located')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Log Source')
        verbose_name_plural = _('Log Sources')
    
    def __str__(self):
        return f"{self.get_source_type_display()} - {self.host}:{self.port}"


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
