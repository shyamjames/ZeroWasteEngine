from django.apps import AppConfig


class FoodFlashConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.food_flash'

    def ready(self):
        import apps.food_flash.signals
