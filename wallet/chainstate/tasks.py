import requests
from decimal import Decimal
from typing import Union, List, Optional, Dict
from jsonrpcclient import parse,Ok



from wallet.models import Token
from wallet.chainstate.models import State
from wallet.chainstate.utils import request_token_balance

from test_app.celery import app
from celery.utils.log import get_task_logger as getLogger
logger = getLogger(__name__)

@app.task()
def check_address_status(chain:str=None):
    """
    检查所有 State 表下的钱包地址余额状态
    若余额发生变化，则更新 is_update、usdt_balance、query_count字段
    否则仅更新query_count字段
    """
    updated_count = 0
    if chain is None or chain.upper() == 'ETH':
        updated_count = check_all_address_status('ETH')
    if chain is None or chain.upper() == 'TRX':
        updated_count = updated_count + check_all_address_status('TRX')

    return updated_count


def get_eth_address_balance(state_obj:'State', token_obj:'Token'):
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
        return value
    return None

def get_trx_address_balance(state_obj:'State', token_obj:'Token'):
    addr_obj = state_obj.address
    # 构建地址代币余额请求接口
    from wallet.helpers import get_trc20_balance

    trc20_value = get_trc20_balance(addr_obj.address, token_obj.contract_address)
    
    return trc20_value / (10**token_obj.token_decimal)

    # host_url = "https://apilist.tronscan.org/api/account/tokens"
    # token_info_url = f"{host_url}?address={addr_obj.address}&token={token_obj.token_symbol}"
    #                 #&start=0&limit=20&hidden=0&show=0&sortType=0"

    # # 检测代币值变化
    # response = requests.get(
    #     token_info_url
    # )
    # parsed_data = response.json()['data']

    # # 寻找当前检测代币合约地址的对象
    # for data in parsed_data:
    #     if token_obj.contract_address == data['tokenId']:
    #         value:Decimal = Decimal(data['quantity']).quantize(Decimal('0.000000'))
    #         return value
    # return None


def check_all_address_status(chain = 'TRX'):
    """
    检测波场地址的余额状态
    """
    chain_upper = chain.upper()
    get_address_balance = get_eth_address_balance
    if 'TRX' == chain_upper:
        get_address_balance = get_trx_address_balance

    # 获取波场链下所有代币
    token_objs = Token.objects.filter(chain__chain_symbol=chain_upper)

    update_count = 0
    for token_obj in token_objs:
        # 寻找符合对应公链地址的待检测对象
        state_objs = State.objects.filter(
            is_active=True,
            rpc__chain=token_obj.chain,is_update=False,
        )[:20]
        for state_obj in state_objs:
            try:
                state_obj.balance = get_address_balance(
                    state_obj=state_obj,
                    token_obj=token_obj
                )
        
                if state_obj.is_update:
                    update_count = update_count + 1
                state_obj.flush()
            except Exception as e:
                logger.error(f"{state_obj.address} get balance error",exc_info=e.args)
                raise e
    return update_count