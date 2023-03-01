from django.apps import AppConfig


class CollectingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collecting'
    verbose_name = 'Приложение для сбора'
