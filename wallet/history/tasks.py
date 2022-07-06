import requests,json
from decimal import Decimal
from typing import Union, List, Optional, Dict
from jsonrpcclient import parse,Ok

from requests.exceptions import SSLError

from django.db import transaction
from django.utils import timezone, datetime_safe as datetime
from django.db.utils import IntegrityError

from wallet.models import Token
from wallet.helpers import transfer_trc20_tron
from wallet.chainstate.models import State
from wallet.history import constant
from wallet.history.models import Deposit,Withdraw

from django.conf import settings
from libraries.celery import app
from celery.utils.log import get_task_logger as getLogger
logger = getLogger(__name__)

@app.task()
def check_address_deposit(chain:str=None):
    """
    检查State处于is_update=True的所有地址
    尝试下载地址的交易,成功则自动新增Deposit实例数据
    若地址尝试下载发现交易已经存在,则将is_update字段修改为False
    """
    updated_count = 0
    if chain is None or chain.upper() == 'ETH':
        updated_count = check_eth_address_deposit()
    if chain is None or chain.upper() == 'TRX':
        updated_count = updated_count + check_trx_address_deposit()

    return updated_count

def check_eth_address_deposit():
    update_count = 0

    state_objs = State.objects.filter(
        rpc__chain__chain_symbol='ETH',is_update=True
    )[:20]

    for obj in state_objs:
        address = obj.address

    return update_count

def check_trx_address_deposit():
    """
    检查波场充值情况,只追查最近25笔充值
    若用户连续充值高于此限额,则会漏充值记录
    """
    update_count = 0
    
    # 获取所有代币
    tokens = Token.objects.filter(
        chain__chain_symbol = "TRX"
    )

    # 获取所有更新地址
    state_objs = State.objects.filter(
        rpc__chain__chain_symbol='TRX',is_update=True
    )[:20]

    host_url = "https://apilist.tronscan.org/api/token_trc20/transfers"
    # https://apilist.tronscan.org/api/token_trc20/transfers?
    # limit=20&start=0&sort=-timestamp&count=true&
    # toAddress=TQ3UsrgH4nCyjxze6tqTZoCax54WVmmRkS&
    # tokens=TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t&
    # relatedAddress=TQ3UsrgH4nCyjxze6tqTZoCax54WVmmRkS
    for token in tokens:
        for state in state_objs:
            try:
                request_url = f"{host_url}?limit=50&start=0&sort=-timestamp&count=true" \
                    f"&tokens={token.contract_address}&relatedAddress={state.address}&toAddress={state.address}"
                response = requests.get(request_url).json()
                token_transfer_list = response['token_transfers']
            except Exception as e:
                logger.error(f"请求{request_url}时网络或参数发生错误",exc_info=e.args)
                break

            try:
                for transfer in token_transfer_list:
                    if transfer['to_address'] != state.address.address:
                        # 忽略非充值类交易
                        continue

                    if transfer['contractRet'] != 'SUCCESS' \
                        or transfer['finalResult'] != 'SUCCESS':
                        # 忽略异常交易
                        logger.warning(f"发生一笔未知的错误交易:{transfer['transaction_id']}")
                        continue

                    if transfer['fromAddressIsContract']:
                        # 忽略合约充值
                        logger.warning(f"发生了一笔合约转入:{transfer['transaction_id']}")
                        continue
                    
                    timestamp = transfer['block_ts'] / 1000
                    
                    deposit = Deposit()
                    deposit.txid                    = transfer['transaction_id']
                    deposit.counterparty_address    = transfer['from_address']
                    deposit.deposit_address         = transfer['to_address']
                    deposit.deposit                 = state.address
                    deposit.amount                  = Decimal(transfer['quant']) / (10 ** token.token_decimal)
                    deposit.token                   = token if token.contract_address == transfer['contract_address'] else None
                    deposit.block_time              = timezone.datetime.fromtimestamp(timestamp,timezone.utc)
                    deposit.save()
                    update_count = update_count + 1
            except IntegrityError as e:
                # TXID已经存在
                state.is_update = False
                state.save(update_fields=['is_update'])

                logger.debug(f"{state.address} 无更新的交易",exc_info=e.args)
                

    return update_count


def check_trx_deposit_hsitory():
    """
    检查交易是否真实
    """
    update_count = 0
    history = Deposit.objects.filter(
        status=constant.SUBMITTED,
        token__chain__chain_symbol = "TRX"
    )[:20]

    for order in history:
        try:
            host_url = 'https://api.trongrid.io/event/transaction'
            request_url = f"{host_url}/{order.txid}"
            response = requests.get(request_url).json()[0]
            if response['event'] == 'Transfer(address indexed from, address indexed to, uint256 value)' \
                and response['contract_address'] == order.token.contract_address:
                
                order.status = constant.AUDITED
                
                order.save(update_fields=['status'])
                update_count = update_count + 1
        except Exception as e:
            logger.error(f"未知错误:{request_url}",exc_info=e.args)
            order.status = constant.ERROR
            order.save(update_fields=['status'])

    return update_count


@app.task()
def check_trx_withdraw():
    # test
    update_count = 0
    history = Withdraw.objects.filter(
        status=constant.AUDITED,
        token__chain__chain_symbol = "TRX"
    )[:20]

    for order in history:
        try:
            with transaction.atomic():
                # 锁定订单
                if order.status != Withdraw.objects.get(pk=order.pk).status:
                    logger.warning("状态发生非预期的行为")
                    continue
                order.status = constant.WITHDRAWING
                order.save(update_fields=["status"])

                # 构建转账
                token_obj = order.token
                address = order.counterparty_address
                amount = order.amount * (10 ** token_obj.token_decimal)
                contract_address = token_obj.contract_address
                chain_network = token_obj.chain.chain_network
                result = transfer_trc20_tron(
                    address, 
                    int(amount),
                    "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", 
                    contract_address, 
                    chain_network
                )
                
                # 填补订单信息
                order.txid = result['id']
                order.block_time = timezone.datetime.fromtimestamp(int(result['blockTimeStamp']) / 1000,timezone.utc)
                order.success_info = json.dumps(result)
                order.save(
                    update_fields=[
                        'txid','block_time',
                        'success_info'
                    ]
                )
        except SSLError as e:
            logger.error("网络连接错误")
        except Exception as e:
            logger.error(f"未知错误:{e.args}")
            order.error_info = e.args
            order.status = constant.ERROR
            order.save(update_fields=["error_info","status"])
            continue
