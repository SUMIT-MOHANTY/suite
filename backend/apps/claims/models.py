from django.db import models
from apps.core.models import TimestampedModel, AuditMixin

CLAIM_STATUS = [
    ("OPEN", "Open"),
    ("CLOSED", "Closed"),
    ("REOPENED", "Reopened"),
]


class Claim(TimestampedModel, AuditMixin):
    policy = models.ForeignKey(
        "policies.Policy", on_delete=models.CASCADE, related_name="claims"
    )
    claim_number = models.CharField(max_length=50, unique=True)
    loss_date = models.DateField()
    reported_date = models.DateField()
    amount_claimed = models.DecimalField(max_digits=15, decimal_places=2)
    amount_reserved = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20, choices=CLAIM_STATUS, default="OPEN"
    )

    class Meta:
        db_table = "claims_claim"
        indexes = [models.Index(fields=["loss_date"])]

    def __str__(self):
        return self.claim_number
