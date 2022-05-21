from django.core.management.base import BaseCommand

from logging import getLogger
logger = getLogger(__name__)
       

class Command(BaseCommand):
    help = """
    Create Deposit Address: 
    
    python manage.py create_deposit_address -u [username or uid]
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass




    