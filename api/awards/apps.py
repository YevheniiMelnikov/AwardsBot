from django.apps import AppConfig


class AwardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.awards"

    def ready(self):
        import api.awards.signals
