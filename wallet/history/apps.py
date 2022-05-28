from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HistoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallet.history'
    verbose_name = _('Wallet History')
