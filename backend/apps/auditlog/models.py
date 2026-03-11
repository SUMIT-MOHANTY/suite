from django.db import models


class AuditLog(models.Model):
    ACTION_CH = [("CREATE", "Create"), ("UPDATE", "Update"), ("DELETE", "Delete")]

    id = models.BigAutoField(primary_key=True)
    table_name = models.CharField(max_length=50)
    object_id = models.IntegerField()
    action = models.CharField(max_length=10, choices=ACTION_CH)
    changes = models.JSONField(default=dict)
    user_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auditlog_auditlog"
        indexes = [
            models.Index(fields=["table_name"]),
            models.Index(fields=["object_id"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"{self.action} on {self.table_name} #{self.object_id}"
