from django.apps import AppConfig


class BasicAppConfig(AppConfig):
    name = 'basic_app'

    def ready(self):
        import users.signals
