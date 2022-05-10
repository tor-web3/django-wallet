from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from wallet.models import (
    Pubkey,
    Chain,
    Address,
)
from wallet.helpers import *


class HelpersTestCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            pk=1,
        )        

    def test_get_deposit_address(self):
        address = get_deposit_address(self.user, "TRX")
        self.assertEqual(address,'TQZmyGG5NBvE7NQSshHk4P1yuNJXcBkh3H',"error")