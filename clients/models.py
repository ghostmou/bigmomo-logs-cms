from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    """Client model representing organizational clients."""
    
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        help_text=_('Name of the client organization')
    )
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='created_clients',
        verbose_name=_('Created By')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_project_count(self):
        """Return the number of projects for this client."""
        return self.projects.count()
