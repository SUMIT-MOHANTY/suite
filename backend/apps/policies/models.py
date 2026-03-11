import reversion
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.core.models import AuditMixin
from .constants import PolicyStatus

@reversion.register()
class Policy(AuditMixin):
    captive         = models.ForeignKey('captives.Captive', on_delete=models.CASCADE, related_name='policies')
    policy_number   = models.CharField(max_length=100, unique=True)
    effective_date  = models.DateField()
    expiry_date     = models.DateField()
    premium         = models.DecimalField(max_digits=14, decimal_places=2)
    status          = models.CharField(max_length=20, choices=PolicyStatus.choices, default=PolicyStatus.QUOTE)

    def clean(self):
        if self.expiry_date <= self.effective_date:
            raise ValidationError("Expiry date must be after effective date")

    def change_status(self, new_status: PolicyStatus):
        allowed_map = {
            PolicyStatus.QUOTE:    [PolicyStatus.BINDER, PolicyStatus.CANCELLED],
            PolicyStatus.BINDER:   [PolicyStatus.ISSUED, PolicyStatus.CANCELLED],
            PolicyStatus.ISSUED:   [PolicyStatus.QUOTENOTICE, PolicyStatus.ENDORSED, PolicyStatus.RENEWED, PolicyStatus.CANCELLED],
            PolicyStatus.ENDORSED: [PolicyStatus.ISSUED],
            PolicyStatus.RENEWED:  [],
            PolicyStatus.CANCELLED: [PolicyStatus.QUOTE, PolicyStatus.BINDER, PolicyStatus.ISSUED],
            PolicyStatus.EXPIRED:  [],
        }
        if new_status not in allowed_map.get(self.status, []):
            raise ValidationError(f"Cannot transition from {self.status} to {new_status}")
        self.status = new_status
        self.save()
