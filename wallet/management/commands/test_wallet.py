from django.core.management.base import BaseCommand

from logging import getLogger
logger = getLogger(__name__)
       
from wallet.monero.backends.offline import OfflineWallet, WalletIsOffline
from wallet.monero.backends.jsonrpc.wallet import JSONRPCWallet
from wallet.monero.wallet import Wallet
from wallet.monero.account import Account
from decimal import Decimal
import time

class Command(BaseCommand):
    help = """
    Create Deposit Address: 
    
    python manage.py create_deposit_address -u [username or uid]
    """

    # def add_arguments(self, parser):
    #     self.username_help = 'User Unique username (Required)'
    #     parser.add_argument('-u','--username', nargs='?', type=str,
    #                         help=self.username_help)
    #     parser.add_argument('-c','--chain', nargs='?', type=str,
    #                         help='Generate wallet address based on blockchain.(default: TRX)')
    #     parser.add_argument('-i','--index', nargs='?', type=int,
    #                         help='Each user has an independent set of address numbers, and '\
    #                             'addresses with the same number are the same.(default: new address)')
    def test(self):
        addr = "47ewoP19TN7JEEnFKUJHAYhGxkeTRH82sf36giEp9AcNfDBfkAtRLX7A6rZz18bbNHPNV7ex6WYbMN3aKisFRJZ8Ebsmgef"
        svk = "6d9056aa2c096bfcd2f272759555e5764ba204dd362604a983fa3e0aafd35901"
        ssk = "e0fe01d5794e240a26609250c0d7e01673219eececa3f499d5cfa20a75739b0a"

        from wallet.monero.seed import Seed
        from wallet.monero import ed25519

        from wallet.monero.backends.offline import OfflineWallet, WalletIsOffline
        from wallet.monero.wallet import Wallet

        # seed = Seed("paper inline drowning tsunami romance software layout sowed hold bikini duration stick hubcaps dash biggest lagoon popular sack ecstatic ouch taken rounded else fidget dash")
        # seed = Seed("2eb824cd1f2aff1091ec9995ddecab96e70cc4ed59cfd611fbc902358bba0e0c")
        # # print(seed.hex_seed())
        
        # print(seed.public_address())
        # print(seed.secret_view_key())
        # # print(seed.secret_spend_key())
        # print("public_view_key")
        # print(ed25519.public_from_secret_hex(seed.secret_view_key()))
        # print(seed.public_view_key())
        # print("public_spend_key")
        # print(ed25519.public_from_secret_hex(seed.secret_spend_key()))
        # print(seed.public_spend_key())
        
        wallet = Wallet(
            OfflineWallet("48NLPW7hugSV3MuXcLKmLzTvyZ4twYu9sWza8zz5Q6ueiocKWvz6QHUSxEwdTWgidNYv4C5AiGLFc4vCNU7bdkRf5R9BRob",
             view_key="bdb9bc040c690bfccc6f4fdca66a705a046ac3402ccc2c38bb72f2aef3768900")
            # OfflineWallet(seed.public_address(), view_key=seed.secret_view_key(), spend_key=seed.public_spend_key())
            # OfflineWallet(seed.public_address(), view_key=seed.secret_view_key(), spend_key=seed.secret_spend_key())
        )
        # print(wallet.new_address())

        print(wallet.get_address(0, 0))
        print(wallet.get_address(1, 1))
        print(wallet.get_address(1, 1).view_key())
        
        wallet = Wallet(
            OfflineWallet(wallet.get_address(1, 1),
             view_key=wallet.get_address(1, 1).view_key())
            # OfflineWallet(seed.public_address(), view_key=seed.secret_view_key(), spend_key=seed.public_spend_key())
            # OfflineWallet(seed.public_address(), view_key=seed.secret_view_key(), spend_key=seed.secret_spend_key())
        )
        print(wallet.get_address(0, 0))


    def handle(self, *args, **options):
        # TODO: 存入可执行后端, 获取当前有余额的用户索引, 统一提币转账
        value = 0.0001
        to_address = "73a4nWuvkYoYoksGurDjKZQcZkmaxLaKbbeiKzHnMmqKivrCzq5Q2JtJG1UZNZFqLPbQ3MiXCk2Q5bdwdUNSr7X9QrPubkn"
        my_address = "597VQuGFFuBCyj25D8svLQUCQZbpKaPFdCtdnAbYevD44pzyRxczbcaBJLkY6sLz9bA84iMxvFRbu5vFPBHxiTWAJWuqBkM"
        i = 0
        while True:
            try:
                w = Wallet(JSONRPCWallet(port=38088))
                # print(w.incoming())
                saddress = w.get_address(0, 0)
                for act in w.accounts:
                    timer = int(time.time())
                    address = saddress.with_payment_id(i)
                    try:
                        # print(act.wallet.view_key())
                        # print(act.wallet.address())
                        # 检查账户余额
                        # TODO: 将余额更新到数据库中,如果有更新的话
                        all_account_balance = act.balances()
                        account_balance = all_account_balance[1]
                        transfer_amount = Decimal(str(value))
                        surplus_amount = (account_balance - transfer_amount) / 2
                        # 若足以支付订单余额,则进行转账,并将剩余资金流入找零地址
                        if account_balance > Decimal("0.000071707920"):
                            txns = act.sweep_all(address)
                            # txns = act.transfer_multiple([
                            #     (to_address, transfer_amount),
                            #     (my_address, surplus_amount / 2),
                            #     (address, surplus_amount / 2),
                            # ])
                            print(txns[0])
                            with open("runtime/xmr_transfer2.log","a+") as f:
                                f.writelines(f"{act.index},{txns[0][0].hash},{address},{timer},{txns[0][1]}\n")
                            if txns:
                                i = i + 1
                        # TODO:记录剩余余额变化情况
                    except Exception as e:
                        print(e.args)
                        time.sleep(0.5)
            except Exception as e:
                print(e.args)
            time.sleep(10)

    