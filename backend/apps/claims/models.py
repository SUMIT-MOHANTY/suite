from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class ClaimStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    IN_REVIEW = 'in_review', 'Under Review'
    APPROVED = 'approved', 'Approved'
    DENIED = 'denied', 'Denied'
    CLOSED = 'closed', 'Closed'

class Claim(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    claim_number = models.CharField(max_length=50, unique=True)
    policy_number = models.CharField(max_length=50, db_index=True)
    claimant_name = models.CharField(max_length=200)
    claimant_email = models.EmailField()
    incident_date = models.DateField()
    incident_desc = models.TextField()
    status = models.CharField(max_length=20, choices=ClaimStatus.choices, default=ClaimStatus.DRAFT)
    adjuster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reserve_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.claim_number} - {self.claimant_name}"

class ClaimTimeline(TimeStampedModel):
    claim = models.ForeignKey(Claim, related_name='timeline_events', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    description = models.TextField()
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
