from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.auth"

    def ready(self):
        from . import signals  # noqa: F401
