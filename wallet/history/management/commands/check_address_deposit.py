from django.core.management.base import BaseCommand

from logging import getLogger
logger = getLogger(__name__)
       

class Command(BaseCommand):
    help = """
    Check address deposit
    
    python manage.py check_address_deposit -c eth
    """

    def add_arguments(self, parser):
        parser.add_argument('-c','--chain', nargs='?', type=str,
                            help='check wallet address deposit history based on blockchain.(default: ALL)')

    def handle(self, *args, **options):
        from wallet.history.tasks import check_address_deposit,check_trx_deposit_hsitory

        chain = options['chain'] if options['chain'] else None
        
        updated_count = check_address_deposit(chain)
        print(f"There are {updated_count} wallet addresses deposit behavior.")

        updated_count = check_trx_deposit_hsitory()
        print(f"There are {updated_count} wallet addresses deposit behavior.")
    

    