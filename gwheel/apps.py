from django.apps import AppConfig

class GwheelConfig(AppConfig):
    name = 'gwheel'

    def ready(self):
        import gwheel.signals