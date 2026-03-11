from django.contrib.auth import get_user_model
from django.db import models
from apps.core.models import TimestampedModel, AuditMixin

User = get_user_model()

JURISDICTION_CHOICES = [
    ("AVG", "Anguilla"),
    ("CYM", "Cayman"),
    ("VGB", "BVI"),
    ("BMA", "Bermuda"),
    ("DMH", "Domicile Other"),
]

CAPTIVE_STATUS = [
    ("ACTIVE", "Active"),
    ("INACTIVE", "Inactive"),
    ("WIND_UP", "Wind-up"),
]


class Captive(TimestampedModel, AuditMixin):
    name = models.CharField(max_length=255, unique=True)
    jurisdiction = models.CharField(max_length=3, choices=JURISDICTION_CHOICES)
    formation_date = models.DateField()
    minimum_capital = models.BigIntegerField(default=0)
    paid_up_capital = models.BigIntegerField(default=0)
    surplus = models.BigIntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=CAPTIVE_STATUS, default="ACTIVE"
    )

    class Meta:
        db_table = "captives_captive"
        unique_together = [["name", "jurisdiction"]]
        indexes = [
            models.Index(fields=["jurisdiction"]),
            models.Index(fields=["formation_date"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.jurisdiction}"
