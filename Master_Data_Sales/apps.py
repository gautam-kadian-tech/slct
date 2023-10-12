from django.apps import AppConfig


class MasterDataManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Master_Data_Sales"


def ready(self):
    import Master_Data_Sales.signals
