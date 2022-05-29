import config

from hdwallet import HDWallet
from hdwallet.utils import generate_mnemonic
from hdwallet.symbols import TRX as SYMBOL
from typing import Optional

import json
def test_generate_mnemonic():
    # Choose strength 128, 160, 192, 224 or 256
    STRENGTH: int = 160  # Default is 128
    # Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
    LANGUAGE: str = "english"  # Default is english
    # Generate new entropy hex string
    MNEMONIC: str = generate_mnemonic(language=LANGUAGE,strength=STRENGTH)
    # Secret passphrase for mnemonic
    PASSPHRASE: Optional[str] = None  # "meherett"

    # Initialize Bitcoin mainnet HDWallet
    hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)
    # Get Bitcoin HDWallet from entropy
    hdwallet.from_mnemonic(
        mnemonic=MNEMONIC#,  passphrase=PASSPHRASE
    )

    # Derivation from path
    # hdwallet.from_path("m/44'/0'/0'/0/0")
    # Or derivation from index

    hdwallet.from_index(44, hardened=True)
    hdwallet.from_index(195, hardened=True)
    hdwallet.from_index(0, hardened=True)
    hdwallet.from_index(0)
    hdwallet.from_index(0)
    
    # Print all Bitcoin HDWallet information's
    # print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))
    return hdwallet.p2pkh_address(),hdwallet.mnemonic()
    

def write_value(values):
    address = values[0].lower()
    if address[-1] == address[-2]:
        with open(f'./address{1}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
        if address[-2] == address[-3]:
            with open(f'./address{2}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
            if address[-3] == address[-4]:
                with open(f'./address{3}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
                if address[-4] == address[-5]:
                    with open(f'./address{4}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
                    if address[-5] == address[-6]:
                        with open(f'./address{5}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
                        if address[-6] == address[-7]:
                            with open(f'./address{6}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
                            if address[-7] == address[-8]:
                                with open(f'./address{7}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
    if address[2] == address[3]:
        with open(f'./address_{1}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
        if address[3] == address[4]:
            with open(f'./address_{2}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
            if address[4] == address[5]:
                with open(f'./address_{3}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
                if address[5] == address[6]:
                    with open(f'./address_{4}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
                    if address[6] == address[7]:
                        with open(f'./address_{5}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
                        if address[7] == address[8]:
                            with open(f'./address_{6}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')
                            if address[8] == address[9]:
                                with open(f'./address_{7}.csv', 'a+') as load_f :load_f.writelines(f'{values[0]},{values[1]}\n')

for d in range(10000):
    for i in range(10000):
        values = test_generate_mnemonic()
        write_value(values)
    #     break
    # break