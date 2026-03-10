from django.db import migrations


ROLES = ["admin", "underwriter", "accounting_mgr", "relationship_mgr", "claims_mgr", "compliance_officer"]


def create_role_groups(apps, _schema_editor):
    Group = apps.get_model("auth", "Group")
    for role in ROLES:
        Group.objects.get_or_create(name=role)


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_add_role_field"),
    ]
    operations = [migrations.RunPython(create_role_groups)]
