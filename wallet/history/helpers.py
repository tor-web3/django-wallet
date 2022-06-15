
from functools import partial

from tronpy import Tron, Contract
from tronpy import AsyncTron, AsyncContract
from tronpy.keys import PrivateKey

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
    # if 'contractResult' in receipt:
    #     return contract.functions.transfer.parse_output(receipt['contractResult'][0])

    # # # result
    # return txn.result()


# generate_eth_address = partial(transfer_trc20_tron, mainnet='ETH')