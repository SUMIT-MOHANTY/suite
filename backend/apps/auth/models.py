from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('underwriter', 'Underwriter'),
        ('accounting_manager', 'Accounting Manager'),
        ('relationship_manager', 'Relationship Manager'),
        ('claims_manager', 'Claims Manager'),
        ('compliance_officer', 'Compliance Officer'),
    ]
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    
    class Meta:
        db_table = 'auth_user'
