from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


class ChainstateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallet.chainstate'
    verbose_name = _('Wallet State')
    
    def ready(self):
        from wallet.chainstate.slots import handle_post_save_address
        from wallet.chainstate import tasks
        
        post_save.connect(handle_post_save_address, sender='wallet.Address')
