import requests,json
from decimal import Decimal
from typing import Union, List, Optional, Dict
from jsonrpcclient import parse,Ok
from logging import getLogger
logger = getLogger(__name__)

from django.utils import timezone, datetime_safe as datetime
from django.db.utils import IntegrityError

from wallet.models import Token
from wallet.chainstate.models import State

from wallet.history.models import Deposit

def check_address_deposit(chain:str=None):
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

    for token in tokens:
        for state in state_objs:
            try:
                request_url = f"{host_url}?limit=20&start=0&sort=-timestamp&count=true" \
                    f"&tokens={token.contract_address}&relatedAddress={state.address}"
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
                state.is_active = False
                state.is_update = False
                state.save(update_fields=['is_active','is_update'])

                logger.debug(f"{state.address} 无更新的交易",exc_info=e.args)
                

    return update_count