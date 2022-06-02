from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from wallet.models import (
    Pubkey,
    Chain,
    Address,
)
from wallet.helpers import *


# python manage.py test wallet.HelpersTestCase
class HelpersTestCase(TestCase):
    fixtures = ['wallet.json']

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            pk=1,
        )
        

    # python manage.py test wallet.HelpersTestCase.test_generate_deposit_address
    def test_generate_deposit_address(self):
        trx_obj = generate_deposit_trx_address(self.user)
        self.assertEqual(trx_obj.address,'TQZmyGG5NBvE7NQSshHk4P1yuNJXcBkh3H',"deposit error")
        
        eth_obj = generate_deposit_eth_address(self.user)
        self.assertEqual(eth_obj.address,'0xCA1a58A97Cc84285DacE852a5994383A080836a0',"deposit error")
        
        