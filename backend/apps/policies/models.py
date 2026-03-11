from django.db import models
from apps.core.models import TimestampedModel, AuditMixin

POLICY_STATUS = [
    ("BOUND", "Bound"),
    ("ENDORSED", "Endorsed"),
    ("EXPIRED", "Expired"),
    ("CANCELLED", "Cancelled"),
]


class Policy(TimestampedModel, AuditMixin):
    captive = models.ForeignKey(
        "captives.Captive", on_delete=models.CASCADE, related_name="policies"
    )
    policy_number = models.CharField(max_length=50, unique=True)
    inception_date = models.DateField()
    expiration_date = models.DateField()
    limit = models.DecimalField(max_digits=15, decimal_places=2)
    premium = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=POLICY_STATUS, default="BOUND")

    class Meta:
        db_table = "policies_policy"
        indexes = [models.Index(fields=["inception_date"])]

    def __str__(self):
        return self.policy_number
