# import config

try:
    from hdwallet import HDWallet
    from hdwallet.utils import generate_mnemonic
    from hdwallet.symbols import ETH as SYMBOL
except ImportError:
    from wallet.hdwallet import HDWallet
    from wallet.hdwallet.utils import generate_mnemonic
    from wallet.hdwallet.symbols import ETH as SYMBOL

from typing import Optional

import json
def test_generate_mnemonic(mnemonic):
    # Initialize Bitcoin mainnet HDWallet
    hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)
    # Get Bitcoin HDWallet from entropy
    hdwallet.from_mnemonic(
        mnemonic=mnemonic#,  passphrase=PASSPHRASE
    )

    # Derivation from path
    # hdwallet.from_path("m/44'/0'/0'/0/0")
    # Or derivation from index

    hdwallet.from_index(44, hardened=True)
    # hdwallet.from_index(195, hardened=True)# trx
    hdwallet.from_index(60, hardened=True)# eth
    hdwallet.from_index(0, hardened=True)
    hdwallet.from_index(0)
    hdwallet.from_index(0)
    
    # Print all Bitcoin HDWallet information's
    # print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))
    return hdwallet.p2pkh_address(),hdwallet.private_key()
    
# print(test_generate_mnemonic("stumble ozone erosion spike argue advice ladder canoe swear theory follow velvet humble tone park"))