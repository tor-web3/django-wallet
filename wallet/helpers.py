from wallet.models import (
    Pubkey,
    Chain,
    Address,
)
from wallet.constant import *

from wallet.hdwallet import HDWallet
from wallet import app_settings

from logging import getLogger
logger = getLogger(__name__)

def get_deposit_address(user, chain_symbol, index=None, new_address=False) ->Address:
    return generate_address(user, chain_symbol, index, DEPOSIT, new_address)

def get_system_lease_address(user,chain_symbol) -> Address:
    return generate_address(user, chain_symbol,0,SYSTEM_LEASE,False)

def generate_address(user, chain_symbol,index:int=None, type=None, new_address=True) -> Address:
    """
    根据用户ID生成钱包地址, 用户ID不变的情况下. 可以通过调整 index 参数来随意切换地址,地址总是稳定不变的
    """
    try:
        # 查找币种主公钥,没有则根据用户pk创建主公钥
        try:
            pubkey = Pubkey.objects.get(user=user,chain__chain_symbol=chain_symbol)
        except Pubkey.DoesNotExist as e:
            chain = Chain.objects.filter(chain_symbol=chain_symbol).first()

            hdwallet: HDWallet = HDWallet(symbol=chain_symbol, use_default_path=False)
            
            hdwallet.from_xpublic_key(app_settings.ACCOUNT_PUBLIC_KEY(chain_symbol))
            hdwallet.from_path(path=f"m/{user.pk}")

            pubkey = Pubkey.objects.create(
                user=user,
                chain=chain,
                public_key= hdwallet.xpublic_key(),
            )
        
        # 确认最新的地址下标
        if index is None:
            try:
                index=0
                address = Address.objects.filter(user=user,chain__chain_symbol=chain_symbol).order_by("-index").first()
                if address:
                    index = address.index
                if new_address:
                    index = index + 1
            except Address.DoesNotExist as e:
                pass
        
        # 若已经存在该地址则返回，没有则创建
        try:
            return Address.objects.get(user=user,chain__chain_symbol=chain_symbol,index=index)
        except Address.DoesNotExist as e:
            # 创建钱包地址
            hdwallet: HDWallet = HDWallet(symbol=chain_symbol, use_default_path=False)
            hdwallet.from_xpublic_key(pubkey.public_key)
            hdwallet.from_path(path=f"m/{index}")
            address = hdwallet.p2pkh_address()

        return Address.objects.create(
                user=user,
                pubkey=pubkey,
                chain=pubkey.chain,
                index=index,
                type=type,
                address=address
            )
    except Exception as e:
        logger.error(msg="Exception while generating wallet address:", exc_info=e)
