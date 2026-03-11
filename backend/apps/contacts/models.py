from django.contrib.auth import get_user_model
from django.db import models
from apps.core.models import TimestampedModel, AuditMixin

User = get_user_model()

ROLE_CHOICES = [
    ("SHAREHOLDER", "Shareholder"),
    ("DIRECTOR", "Director"),
    ("OFFICER", "Officer"),
    ("BROKER", "Broker"),
    ("ACTUARY", "Actuary"),
    ("OTHER", "Other"),
]


class Contact(TimestampedModel, AuditMixin):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="OTHER")

    class Meta:
        db_table = "contacts_contact"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class CaptiveContact(models.Model):
    REL_CHOICES = [
        ("SHAREHOLDER", "Shareholder"),
        ("DIRECTOR", "Director"),
        ("OFFICER", "Officer"),
    ]
    captive = models.ForeignKey(
        "captives.Captive", on_delete=models.CASCADE, related_name="cc_links"
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="cc_links"
    )
    relationship_type = models.CharField(max_length=30, choices=REL_CHOICES)
    role = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contacts_captivecontact"
        unique_together = [["captive", "contact", "relationship_type"]]

    def __str__(self):
        return f"{self.captive} - {self.contact} ({self.relationship_type})"
