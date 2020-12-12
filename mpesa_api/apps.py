from django.apps import AppConfig
from django.db.models.signals import post_save


class CoreConfig(AppConfig):
    name = "mpesa_api"
    # label = "coree"
    verbose_name = "MPESA API CORE"

    def ready(self):
        import mpesa_api.signals
        # pass
