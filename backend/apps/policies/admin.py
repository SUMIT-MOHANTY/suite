from django.contrib import admin
import reversion

from apps.policies.models import Policy

@admin.register(Policy)
class PolicyAdmin(reversion.admin.VersionAdmin):
    list_display = ("policy_number", "captive", "effective_date", "expiry_date", "status")
    readonly_fields = ("created_at", "updated_at")
