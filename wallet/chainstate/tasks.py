import requests
from typing import Union, List, Optional, Dict
from jsonrpcclient import parse,Ok

from logging import getLogger
logger = getLogger(__name__)

from django.utils import timezone

from wallet.models import Token
from wallet.chainstate.models import State
from wallet.chainstate.utils import request_token_balance


def check_eth_address_status():
    """
    检测以太坊地址的余额状态
    """
    now = timezone.now()
    token_objs = Token.objects.filter(chain__chain_symbol="ETH")
    
    for token_obj in token_objs:
        state_objs = State.objects.filter(
            rpc__chain=token_obj.chain,is_update=False,
            stop_at__gt=now,
        )[:20]
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
                logger.error(parsed.message)
