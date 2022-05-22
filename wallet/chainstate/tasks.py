from wallet.chainstate.signals import wallet_address_updated

from typing import Union, List, Optional, Dict

from celery.utils.log import get_task_logger
import requests
from wallet.chainstate.models import State
from wallet.chainstate.utils import request_token_balance
from wallet.models import Token

from logging import getLogger
logger = getLogger(__name__)

def check_eth_address_status(
    addresses: List[str],
):
    token_objs = Token.objects.filter(chain__chain_symbol="ETH")
    state_objs = State.objects.filter(is_update=False)[:20]
    for state_obj in state_objs:
        for token_obj in token_objs:
            addr_obj = state_obj.address
            
            response = requests.post(
                state_obj.rpc.endpoint,
                json=request_token_balance(
                    addr_obj.address,
                    token_obj.contract_address
                )
            )
                    
            parsed = parsed(response.json())
            if isinstance(parsed, Ok):
                print(parsed.result)
                print(int(parsed.result,16))
            else:
                logging.error(parsed.message)

# check_eth_address_status(["asd"])
    