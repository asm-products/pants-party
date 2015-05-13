from django.apps import AppConfig


class TextJokesConfig(AppConfig):
    name = 'textjokes'

    def ready(self):
        from . import receivers
