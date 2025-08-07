from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model with role-based permissions."""
    
    class UserRole(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        EDITOR = 'editor', _('Editor')
    
    class UserStatus(models.TextChoices):
        ACTIVE = 'active', _('Active')
        BLOCKED = 'blocked', _('Blocked')
        PENDING = 'pending', _('Pending Approval')
    
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.EDITOR,
        verbose_name=_('Role')
    )
    
    status = models.CharField(
        max_length=10,
        choices=UserStatus.choices,
        default=UserStatus.PENDING,
        verbose_name=_('Status')
    )
    
    is_password_changed = models.BooleanField(
        default=False,
        verbose_name=_('Password Changed')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN
    
    @property
    def is_editor(self):
        return self.role == self.UserRole.EDITOR
    
    @property
    def is_active_user(self):
        return self.status == self.UserStatus.ACTIVE
    
    @property
    def is_blocked(self):
        return self.status == self.UserStatus.BLOCKED
    
    @property
    def is_pending(self):
        return self.status == self.UserStatus.PENDING
