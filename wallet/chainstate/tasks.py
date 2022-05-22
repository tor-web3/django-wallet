from wallet.chainstate.signals import wallet_address_updated

from typing import Union, List, Optional, Dict

from celery.utils.log import get_task_logger
import requests
from wallet.chainstate.models import State
from wallet.chainstate.utils import request_token_balance
from wallet.models import Token

from jsonrpcclient import parse,Ok
from logging import getLogger
logger = getLogger(__name__)

def check_eth_address_status():
    token_objs = Token.objects.filter(chain__chain_symbol="ETH")
    for token_obj in token_objs:
        state_objs = State.objects.filter(rpc__chain=token_obj.chain,is_update=False)[:20]
        for state_obj in state_objs:
            addr_obj = state_obj.address
            
            response = requests.post(
                state_obj.rpc.endpoint,
                json=request_token_balance(
                    addr_obj.address,
                    token_obj.contract_address
                )
            )
                    
            parsed = parse(response.json())
            if isinstance(parsed, Ok):
                from decimal import Decimal
                value:Decimal = Decimal(int(parsed.result,16)) / (10 ** 6)
                state_obj.balance=value
                state_obj.flush()
                
            else:
                logging.error(parsed.message)
