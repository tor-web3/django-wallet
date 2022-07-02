from functools import partial
from django.utils.translation import gettext_lazy as _

from wallet.models import (
    Pubkey,
    Chain,
    Address,
)
from wallet.constant import *

from wallet.hdwallet import HDWallet
from wallet import app_settings

from wallet.tronpy import Tron, Contract
from wallet.tronpy import AsyncTron, AsyncContract
from wallet.tronpy.keys import PrivateKey
from wallet.monero.backends.offline import OfflineWallet, WalletIsOffline
from wallet.monero.wallet import Wallet

from logging import getLogger
logger = getLogger(__name__)

def get_deposit_address(user, chain_symbol, index=None, new_address=False) ->Address:
    if chain_symbol == "XMR":
        return generate_xmr_address(user, chain_symbol, index, DEPOSIT, new_address)
    return generate_address(user, chain_symbol, index, DEPOSIT, new_address)

def get_system_lease_address(user,chain_symbol) -> Address:
    return generate_address(user, chain_symbol,0,SYSTEM_LEASE,False)

# 查找币种主公钥,没有则根据用户pk创建主公钥
def get_pubkey(user,chain_symbol) -> Pubkey:
    try:
        return Pubkey.objects.get(user=user,chain__chain_symbol=chain_symbol)
    except Pubkey.DoesNotExist as e:
        chain = Chain.objects.filter(chain_symbol=chain_symbol).first()
        
        if not chain:
            # 如果未获取到链信息
            raise Chain.DoesNotExist(_(f"{chain_symbol} is not yet supported, please add it first."))

        hdwallet: HDWallet = HDWallet(symbol=chain_symbol, use_default_path=False)
        
        hdwallet.from_xpublic_key(app_settings.ACCOUNT_PUBLIC_KEY(chain_symbol))
        hdwallet.from_path(path=f"m/{user.pk}")

        return Pubkey.objects.create(
            user        = user,
            chain       = chain,
            public_key  = hdwallet.xpublic_key(),
        )

def get_user_index(user, chain_symbol, index:int=None, new_address=True):
    # 确认用户正在使用的地址下标
    if index is None:
        try:
            filter_params = {
                "user" : user,
                "chain__chain_symbol" : chain_symbol
            }
            if not new_address:
                filter_params["is_select"] = True

            address = Address.objects.filter(
                **filter_params
            ).order_by("-index").first()
            
            # 确定 Index
            index = (0 if not address else address.index)
            if address and new_address:
                index = index + 1
        except Address.DoesNotExist as e:
            return 0
    return index

def generate_xmr_address(user, chain_symbol, index:int=None, type=None, new_address=True) -> Address:
    
    """
    根据用户ID生成钱包地址, 用户ID不变的情况下. 可以通过调整 index 参数来随意切换地址,地址总是稳定不变的
    """
    try:
        # 确认用户正在使用的地址下标
        index = get_user_index(user,chain_symbol,index,new_address)
        
        # 若已经存在该地址则返回，没有则创建
        ret_address = None
        try:
            ret_address = Address.objects.get(user=user,chain__chain_symbol=chain_symbol,index=index)
            ret_address.wallet_chainstate_state.active()
            ret_address.is_select = True
            ret_address.save(update_fields=['is_select'])
        except Address.DoesNotExist as e:
            # 创建钱包地址
            wallet = Wallet(
                OfflineWallet(
                    address=app_settings.XMR_ADDRESS,
                    view_key=app_settings.XMR_SECRET_VIEW_KEY
                )
            )
            print(user.pk)
            print(index)
            address = wallet.get_address(user.pk, index)

            ret_address = Address.objects.create(
                    user=user,
                    # pubkey=pubkey,
                    chain=Chain.objects.get(chain_symbol=chain_symbol),
                    index=index,
                    type=type,
                    is_select=True,
                    address=address
                )

        # 将新地址设为默认使用地址
        Address.objects.filter(
            user=user,
            chain__chain_symbol=chain_symbol,
            is_select=True
        ).exclude(address=ret_address.address).update(is_select=False)

        return ret_address
    except Exception as e:
        logger.error(msg="Exception while generating wallet address:", exc_info=e)
        return None

def generate_address(user, chain_symbol,index:int=None, type=None, new_address=True) -> Address:
    """
    根据用户ID生成钱包地址, 用户ID不变的情况下. 可以通过调整 index 参数来随意切换地址,地址总是稳定不变的
    """
    try:
        pubkey = get_pubkey(user, chain_symbol)
        
        # 确认用户正在使用的地址下标
        index = get_user_index(user, chain_symbol,index,new_address)
        
        # 若已经存在该地址则返回，没有则创建
        ret_address = None
        try:
            ret_address = Address.objects.get(user=user,chain__chain_symbol=chain_symbol,index=index)
            ret_address.wallet_chainstate_state.active()
            ret_address.is_select = True
            ret_address.save(update_fields=['is_select'])
        except Address.DoesNotExist as e:
            # 创建钱包地址
            hdwallet: HDWallet = HDWallet(symbol=chain_symbol, use_default_path=False)
            hdwallet.from_xpublic_key(pubkey.public_key)
            hdwallet.from_path(path=f"m/{index}")
            address = hdwallet.p2pkh_address()

            ret_address = Address.objects.create(
                    user=user,
                    pubkey=pubkey,
                    chain=pubkey.chain,
                    index=index,
                    type=type,
                    is_select=True,
                    address=address
                )

        # 将新地址设为默认使用地址
        Address.objects.filter(
            user=user,
            chain__chain_symbol=chain_symbol,
            is_select=True
        ).exclude(address=ret_address.address).update(is_select=False)

        return ret_address
    except Exception as e:
        logger.error(msg="Exception while generating wallet address:", exc_info=e)

def transfer_trc20_tron(
    to_address:str,value:int,private_key:str,
    contract_address,
    network
):
    priv_key = PrivateKey(bytes.fromhex(private_key))
    from_address = priv_key.public_key.to_base58check_address()
    client = Tron(network=network)
    contract = client.get_contract(contract_address)
    # print('Balance', contract.functions.balanceOf('TGQgfK497YXmjdgvun9Bg5Zu3xE15v17cu'))

    txn = (
        contract.functions.transfer(to_address, value)
        .with_owner(from_address)
        .fee_limit(5_000_000_000)
        .build()
        .sign(priv_key)
        .inspect()
        .broadcast()
    )
    
    receipt = txn.wait()
    return receipt

def get_trc20_balance(address, contract_address, network="mainnet"):
    client = Tron(network=network)
    contract = client.get_contract(contract_address)
    return contract.functions.balanceOf(address)


def check_address(address,chain_symbol):
    try:
        if chain_symbol == "XMR":
            from monero.address import Address
            Address(address)
            return True, chain_symbol
        elif chain_symbol == "TRX":
            from wallet.tronpy.keys import is_address
            return is_address(address), chain_symbol
        elif chain_symbol == "ETH":
            import re
            return bool(re.match("0x[a-fA-F0-9]{40}$", address)), chain_symbol
    except:
        return False

# generate_eth_address = partial(transfer_trc20_tron, mainnet='ETH')

generate_eth_address = partial(generate_address, chain_symbol='ETH')
generate_trx_address = partial(generate_address, chain_symbol='TRX')

generate_deposit_eth_address = partial(generate_eth_address, type=DEPOSIT)
generate_deposit_trx_address = partial(generate_trx_address, type=DEPOSIT)