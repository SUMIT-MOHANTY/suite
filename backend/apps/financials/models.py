from django.db import models
from apps.core.models import TimestampedModel

TYPE_CHOICES = [
    ("PREMIUM", "Premium"),
    ("CLAIM", "Claim"),
    ("CAPITAL", "Capital"),
    ("REINSURANCE", "Reinsurance"),
    ("OTHER", "Other"),
]


class FinancialRecord(TimestampedModel):
    model_type = models.CharField(max_length=30)
    model_id = models.PositiveIntegerField()
    financial_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    period_start = models.DateField()
    period_end = models.DateField()

    class Meta:
        db_table = "financials_financialrecord"
        unique_together = [
            ["model_type", "model_id", "financial_type", "period_start", "period_end"]
        ]
        indexes = [
            models.Index(fields=["model_type", "model_id"]),
            models.Index(fields=["financial_type"]),
        ]

    def __str__(self):
        return f"{self.financial_type} - {self.amount}"
