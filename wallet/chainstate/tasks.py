import requests
from decimal import Decimal
from typing import Union, List, Optional, Dict

from wallet.helpers import get_trc20_balance
from wallet.models import Token
from wallet.chainstate.models import State,Node
from wallet.chainstate.utils import (
    request_token_balance,
    request_block_by_number,
    request_transaction_receipt
)

from django.conf import settings
from django.db.models import Q
from libraries.celery import app
from celery.utils.log import get_task_logger as getLogger
logger = getLogger(__name__)
from jsonrpcclient import parse,Ok

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
    trc20_value = get_trc20_balance(
        addr_obj.address, 
        token_obj.contract_address,
        token_obj.chain.chain_network,
    )
    
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


def get_all_address_in_trc20_block_from_transcan(block_number):
    # https://apilist.tronscanapi.com/api/token_trc20/transfers?limit=50&start=0&sort=-timestamp&count=true&block=42155000
    address_list = []
    current_index = 0
    endpoint = "https://apilist.tronscanapi.com"
    trc20_transfer_uri = "api/token_trc20/transfers"
    STEP_LENGTH = 50
    params = "limit={step_length}&start={current_index}&sort=-timestamp&count=true&block={block_number}"

    # 获取区块所有交易数据
    while True:
        trc20_params = params.format(step_length=STEP_LENGTH,current_index=current_index,block_number=block_number)
        url = f"{endpoint}/{trc20_transfer_uri}?{trc20_params}"
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning("请求发生错误")
            return
        
        # 解析区块交易
        res_json = response.json()
        total_txs = res_json["total"]
        txs = res_json["token_transfers"]

        # 检验区块新交易条数
        if len(txs) == 0:
            break
        
        # 检验
        for tx in txs:
            from_address = tx["from_address"]
            to_address = tx["to_address"]
            address_list = address_list + [
                from_address,
                to_address
            ]
        else:
            current_index = current_index + STEP_LENGTH
            # 区块交易索引超过预期
            if current_index > total_txs:
                break
    ret_list = list(set(address_list))
    return ret_list


# TIP: 尚未完善,存在RPC请求超时的异常处理
# 可考虑使用浏览器API获取区块代币交易
# https://apilist.tronscanapi.com/api/token_trc20/transfers?limit=50&start=0&sort=-timestamp&count=true&block=42155000
# 2022-07-07 弃用,通过RPC确认余额的方式不适用于多地址环境
def check_address_in_trx_block_from_jsonrpc(node_info:Node):
    # 获取区块信息
    response = requests.post(
        f"{node_info.rpc.endpoint}/jsonrpc",
        json=request_block_by_number(
            node_info.block_number + 1
        )
    )
    
    # 解析区块交易数据
    address_list = []
    parsed = parse(response.json())
    if isinstance(parsed, Ok):
        txs = parsed.result["transactions"]
        from wallet.tronpy.keys import to_base58check_address
        for tx in txs:
            to_address = to_base58check_address(tx["to"])
            from_address =  to_base58check_address(tx["from"])
            address_list = address_list + [
                to_address,
                from_address,
            ]

            if "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t" == to_address:
                txid = tx['hash']
                # TODO USDT代币交易
                response_tx = requests.post(
                    f"{node_info.rpc.endpoint}/jsonrpc",
                    json=request_transaction_receipt(
                        txid
                    )
                )
                
                parsed_tx = parse(response_tx.json())
                topics = parsed_tx.result["logs"][0]["topics"]
                token_from_address = to_base58check_address(f"0x{topics[1][-40:]}")
                token_to_address = to_base58check_address(f"0x{topics[2][-40:]}")
                address_list = address_list + [
                    token_from_address,
                    token_to_address
                ]
        else:
            
            address_set = list(set(address_list))

            # 区块索引递增
            node_info.block_number = int(parsed.result.number,16)
            node_info.save()

    return address_list
    

@app.task()
def check_address_in_block():
    nodes = Node.objects.all()
    address_list = []
    for node in nodes:
        if node.chain.chain_symbol == "TRX":
            if settings.DEBUG == True:
                address_list = address_list + get_all_address_in_trc20_block_from_transcan(42155000)
            else:
                address_list = address_list + get_all_address_in_trc20_block_from_transcan(node.block_number)
            node.block_number = node.block_number + 1
            node.save(update_fields=["block_number"])
    
    # TIP:理论单次 OR 地址不超过500个
    if len(address_list) > 500:
        logger.warning("地址超过500个,请注意参数优化")
    q = Q()
    q.connector = "OR"
    for address in address_list:
        q.children.append(("address__address", address))

    state_objs = State.objects.filter(q)

    for state in state_objs:
        if state.is_update:
            continue
        state.active()
        state.balance = state.balance + Decimal(0.000001)
        state.flush()



