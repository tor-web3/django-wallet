from django.apps import AppConfig


class ChainstateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallet.chainstate'
    
    def ready(self):
        from wallet.chainstate import slots
