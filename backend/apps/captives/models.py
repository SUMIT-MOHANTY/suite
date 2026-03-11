from django.db import models
from django.utils.translation import gettext_lazy as _

class TimestampedModel(models.Model):
    """Base model with timestamp fields"""
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class AuditMixin(models.Model):
    """Base model with audit fields"""
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='%(class)s_created')
    updated_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='%(class)s_updated')

    class Meta:
        abstract = True


class CaptiveModel(TimestampedModel, AuditMixin):
    """Captive entity model"""
    
    JURISDICTION_CHOICES = [
        ('AVG', 'Advanta'),
        ('BVD', 'British Virgin Islands'),
        ('CAY', 'Cayman Islands'),
        ('BER', 'Bermuda'),
        ('LUX', 'Luxembourg'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('PENDING', 'Pending'),
        ('DISSOLVED', 'Dissolved'),
    ]
    
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    jurisdiction = models.CharField(max_length=3, choices=JURISDICTION_CHOICES, verbose_name=_("Jurisdiction"))
    formation_date = models.DateField(verbose_name=_("Formation Date"))
    minimum_capital = models.BigIntegerField(default=0, verbose_name=_("Minimum Capital Required"))
    paid_up_capital = models.BigIntegerField(default=0, verbose_name=_("Paid-up Capital"))
    surplus = models.BigIntegerField(default=0, verbose_name=_("Surplus Amount"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name=_("Status"))
    
    @property
    def min_capital_surplus(self):
        """Derived field: minimum_capital + surplus (read-only)"""
        return self.minimum_capital + self.surplus
    
    @property
    def policy_count(self):
        """Derived field: count of policies (badge for list view)"""
        return getattr(self, '_policy_count', 0)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Captive")
        verbose_name_plural = _("Captives")
        constraints = [
            models.UniqueConstraint(fields=['name', 'jurisdiction'], name='unique_name_jurisdiction')
        ]
        ordering = ['-created_at']
