import requests
from decimal import Decimal
from typing import Union, List, Optional, Dict
from jsonrpcclient import parse,Ok

from logging import getLogger
logger = getLogger(__name__)


from wallet.models import Token
from wallet.chainstate.models import State
from wallet.chainstate.utils import request_token_balance

from test_app.celery import app

@app.task(ignore_result=True)
def check_address_status(chain:str=None):
    updated_count = 0
    if chain is None or chain.upper() == 'ETH':
        updated_count = check_eth_address_status()
    if chain is None or chain.upper() == 'TRX':
        updated_count = updated_count + check_trx_address_status()

    return updated_count

def check_eth_address_status():
    """
    检测以太坊地址的余额状态
    """
    token_objs = Token.objects.filter(chain__chain_symbol="ETH")
    
    update_count = 0
    for token_obj in token_objs:
        state_objs = State.objects.filter(
            rpc__chain=token_obj.chain,is_update=False,
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
                value:Decimal = Decimal(int(parsed.result,16)) / (10 ** 6)
                state_obj.balance=value
                if state_obj.is_update:
                    update_count = update_count+ 1
            else:
                logger.error(parsed.message)
                
            state_obj.flush()

    return update_count
def get_eth_address_balance(addr_obj:'Address', token_obj:'Token'):
    pass

def get_trx_address_balance(addr_obj:'Address', token_obj:'Token'):
    # 构建地址代币余额请求接口
    host_url = "https://apilist.tronscan.org/api/account/tokens"
    token_info_url = f"{host_url}?address={addr_obj.address}&token={token_obj.token_symbol}"
                    #&start=0&limit=20&hidden=0&show=0&sortType=0"

    # 检测代币值变化
    response = requests.get(
        token_info_url
    )
    parsed_data = response.json()['data']

    # 寻找当前检测代币合约地址的对象
    for data in parsed_data:
        if token_obj.contract_address == data['tokenId']:
            value:Decimal = Decimal(data['quantity'])
            return value
    return None

# 特定代币的交易记录：https://apilist.tronscan.org/api/token_trc20/transfers?limit=20&start=0&sort=-timestamp&count=true&tokens=TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t&relatedAddress=TD2jixXEuoFTc8LZ26TpN9eJYiG75Staaa
def check_trx_address_status():
    """
    检测波场地址的余额状态
    """
    # 获取波场链下所有代币
    token_objs = Token.objects.filter(chain__chain_symbol="TRX")

    update_count = 0
    for token_obj in token_objs:
        # 寻找符合对应公链地址的待检测对象
        state_objs = State.objects.filter(
            rpc__chain=token_obj.chain,is_update=False,
        )[:20]
        for state_obj in state_objs:
            addr_obj = state_obj.address

            state_obj.balance = get_trx_address_balance(
                addr_obj=addr_obj,
                token_obj=token_obj
            )
    
            if state_obj.is_update:
                update_count = update_count + 1
            state_obj.flush()
    return update_count