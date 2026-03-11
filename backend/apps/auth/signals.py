from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    roles = ["admin", "underwriter", "accounting_mgr", "relationship_mgr", "claims_mgr", "compliance_officer"]
    for role in roles:
        Group.objects.get_or_create(name=role)
