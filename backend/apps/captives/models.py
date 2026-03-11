from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimestampedModel, AuditMixin

User = get_user_model()


class Captive(TimestampedModel, AuditMixin):
    JURISDICTION_CHOICES = [
        ("AVG", "Advanta"),
        ("BVD", "British Virgin Islands"),
        ("CAY", "Cayman Islands"),
        ("BER", "Bermuda"),
        ("LUX", "Luxembourg"),
        ("DMH", "Domicile Other"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("PENDING", "Pending"),
        ("DISSOLVED", "Dissolved"),
        ("WIND_UP", "Wind-up"),
    ]

    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    jurisdiction = models.CharField(
        max_length=3, choices=JURISDICTION_CHOICES, verbose_name=_("Jurisdiction")
    )
    formation_date = models.DateField(verbose_name=_("Formation Date"))
    minimum_capital = models.BigIntegerField(
        default=0, verbose_name=_("Minimum Capital Required")
    )
    paid_up_capital = models.BigIntegerField(
        default=0, verbose_name=_("Paid-up Capital")
    )
    surplus = models.BigIntegerField(default=0, verbose_name=_("Surplus Amount"))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE",
        verbose_name=_("Status"),
    )

    class Meta:
        db_table = "captives_captive"
        verbose_name = _("Captive")
        verbose_name_plural = _("Captives")
        constraints = [
            models.UniqueConstraint(
                fields=["name", "jurisdiction"],
                name="unique_name_jurisdiction",
            ),
        ]
        indexes = [
            models.Index(fields=["jurisdiction"]),
            models.Index(fields=["formation_date"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.jurisdiction}"

    @property
    def min_capital_surplus(self):
        """Derived field: minimum_capital + surplus (read-only)"""
        return self.minimum_capital + self.surplus

    @property
    def policy_count(self):
        """Derived field: count of policies (badge for list view)"""
        return getattr(self, "_policy_count", 0)
