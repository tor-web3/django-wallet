from functools import partial

from jsonrpcclient import request


def to_32_bytes(data: str) -> str:
    str_0_len = 64 - len(data)
    str_0 = '0' * str_0_len
    return str_0 + data

def request_token_balance(address,contract_address) -> request:
    return request(
        "eth_call",
        params=(
            {
                "from":address,
                "to":contract_address,
                "data":"0x70a08231"+to_32_bytes(address[2:])
            },
            "latest"
        )
    )


def request_block_by_number(block_number:int) -> request:
    return request(
        "eth_getBlockByNumber",
        params=[
            hex(block_number),
            True
        ]
    )


def request_transaction_receipt(txid:str) -> request:
    return request(
        "eth_getTransactionReceipt",
        params=[
            txid
        ]
    )
