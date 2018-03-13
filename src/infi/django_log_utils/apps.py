from django.apps import AppConfig

class Config(AppConfig):

    name = 'infi.django_log_utils'
    verbose_name = 'Django Log Utils'

    def ready(self):
        # Register signal handlers
        from . import signals
