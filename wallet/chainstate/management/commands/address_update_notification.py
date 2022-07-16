from django.core.management.base import BaseCommand

from logging import getLogger
logger = getLogger(__name__)
       

class Command(BaseCommand):
    help = """
    Check address status
    
    python manage.py check_address_status -c eth
    """

    def add_arguments(self, parser):
        parser.add_argument('-c','--chain', nargs='?', type=str,
                            help='check wallet address status based on blockchain.(default: ALL)')

    def handle(self, *args, **options):
        from wallet.chainstate.tasks import address_update_notification
        address_update_notification()

    