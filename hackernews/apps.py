from django.apps import AppConfig


class HackernewsConfig(AppConfig):
    name = 'hackernews'

    def ready(self):
        from .api.timeloop import tl
        tl.start()
