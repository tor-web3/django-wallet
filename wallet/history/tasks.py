import requests
from typing import Union, List, Optional, Dict
from jsonrpcclient import parse,Ok

from logging import getLogger
logger = getLogger(__name__)

from django.utils import timezone

from wallet.models import Token
from wallet.chainstate.models import State
from wallet.chainstate.utils import request_token_balance


def check_address_deposit(chain:str=None):
    updated_count = 0
    if chain is None or chain.upper() == 'ETH':
        updated_count = check_eth_address_deposit()
    if chain is None or chain.upper() == 'TRX':
        updated_count = updated_count + check_trx_address_deposit()

    return updated_count

def check_eth_address_deposit():
    update_count = 0
    return update_count

# 特定代币的交易记录：https://apilist.tronscan.org/api/token_trc20/transfers?limit=20&start=0&sort=-timestamp&count=true&tokens=TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t&relatedAddress=TD2jixXEuoFTc8LZ26TpN9eJYiG75Staaa
def check_trx_address_deposit():
    update_count = 0
    return update_count