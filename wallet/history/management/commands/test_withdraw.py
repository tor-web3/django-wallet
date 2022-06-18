
import os, django
from django.core.management.base import BaseCommand

from logging import getLogger
logger = getLogger(__name__)
       

class Command(BaseCommand):
    help = "Runs Pooling."

    # def add_arguments(self, parser):
    #     parser.add_argument('prvate_key', nargs='+', type=str)

    def handle(self, *args, **options):
        django.setup()
        from tgbot.handlers.base.helpers import withdraw
        from django.contrib.auth import get_user_model
        from wallet.history.tasks import check_trx_withdraw
        check_trx_withdraw()
        # withdraw(
        #     get_user_model().objects.get(id=7),
        #     "TS9KNUVtUwFTEQVww28a6ZGiDDS5EKvDAJ",
        #     12,"USDT"
        # )