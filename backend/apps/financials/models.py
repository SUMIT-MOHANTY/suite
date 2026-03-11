from django.db import models
from apps.core.models import AuditMixin

class Invoice(AuditMixin):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    policy = models.ForeignKey(
        'policies.Policy', on_delete=models.CASCADE, related_name='invoices'
    )
    captive = models.ForeignKey(
        'captives.Captive', on_delete=models.CASCADE, related_name='invoices'
    )
    due_date = models.DateField()
    invoice_number = models.CharField(max_length=32, unique=True)
    lines = models.JSONField(default=list)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='draft')
    issued_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class Statement(AuditMixin):
    captive = models.ForeignKey(
        'captives.Captive', on_delete=models.CASCADE, related_name='statements'
    )
    year = models.IntegerField()
    month = models.IntegerField()
    generated_at = models.DateTimeField(auto_now_add=True)
    lines = models.JSONField(default=list)

    class Meta:
        ordering = ['-year', '-month']
        unique_together = [['captive', 'year', 'month']]


TYPE_CHOICES = [
    ("PREMIUM", "Premium"),
    ("CLAIM", "Claim"),
    ("CAPITAL", "Capital"),
    ("REINSURANCE", "Reinsurance"),
    ("OTHER", "Other"),
]

class FinancialRecord(models.Model):
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
