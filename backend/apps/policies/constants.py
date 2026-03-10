from django.db import models

class PolicyStatus(models.TextChoices):
    QUOTE          = "quote", "Quote"
    BINDER         = "binder", "Binder"
    ISSUED         = "issued", "Issued"
    EXPIRED        = "expired", "Expired"
    CANCELLED      = "cancelled", "Cancelled"
