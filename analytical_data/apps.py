from django.apps import AppConfig


class AnalyticalDataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "analytical_data"

    def ready(self):
        import analytical_data.utils.signals
