from django.core.management.base import BaseCommand

from logging import getLogger
logger = getLogger(__name__)
       

class Command(BaseCommand):
    help = """
    Create Deposit Address: 
    
    python manage.py create_deposit_address -u [username or uid]
    """

    def add_arguments(self, parser):
        self.username_help = 'User Unique username (Required)'
        parser.add_argument('-u','--username', nargs='?', type=str,
                            help=self.username_help)
        parser.add_argument('-c','--chain', nargs='?', type=str,
                            help='Generate wallet address based on blockchain.(default: TRX)')
        parser.add_argument('-i','--index', nargs='?', type=int,
                            help='Each user has an independent set of address numbers, and '\
                                'addresses with the same number are the same.(default: new address)')

    def handle(self, *args, **options):
        from wallet.helpers import get_deposit_address
        from django.contrib.auth import get_user_model

        try:
            username = options.get('username',None)
            user = get_user_model().objects.get(username=username)
        except Exception as e:
            logger.warning(f"{self.username_help}")
            logger.error(e.args)
            return

        chain = options['chain'] if options['chain'] else "TRX"
        index = options['index'] if options['index'] else -1

        
        new = False
        if index < 0:
            index = None
            new = True

        print(get_deposit_address(user,chain.upper(),index,new))
    




    