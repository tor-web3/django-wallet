from django.core.management.base import BaseCommand

from logging import getLogger
logger = getLogger(__name__)
       

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

    def handle(self, *args, **options):
        addr = "47ewoP19TN7JEEnFKUJHAYhGxkeTRH82sf36giEp9AcNfDBfkAtRLX7A6rZz18bbNHPNV7ex6WYbMN3aKisFRJZ8Ebsmgef"
        svk = "6d9056aa2c096bfcd2f272759555e5764ba204dd362604a983fa3e0aafd35901"
        ssk = "e0fe01d5794e240a26609250c0d7e01673219eececa3f499d5cfa20a75739b0a"

        from wallet.monero.seed import Seed
        from wallet.monero import ed25519

        from wallet.monero.backends.offline import OfflineWallet, WalletIsOffline
        from wallet.monero.wallet import Wallet

        seed = Seed("尤 洗 综 吴 恢 势 课 哲 目 柯 涉 免 频 楚 客 中 竞 休 者 介 润 舰 太 项 综","Chinese (simplified)")
        print(seed.public_address())
        # print(seed.secret_view_key())
        # print(seed.secret_spend_key())
        print("public_view_key")
        print(ed25519.public_from_secret_hex(seed.secret_view_key()))
        print(seed.public_view_key())
        print("public_spend_key")
        print(ed25519.public_from_secret_hex(seed.secret_spend_key()))
        print(seed.public_spend_key())
        
        wallet = Wallet(
            # OfflineWallet(seed.public_address(), view_key=seed.secret_view_key())
            OfflineWallet(seed.public_address(), view_key=seed.secret_view_key(), spend_key=seed.public_spend_key())
            # OfflineWallet(seed.public_address(), view_key=seed.secret_view_key(), spend_key=seed.secret_spend_key())
        )
        # print(wallet.new_address())

        print(wallet.get_address(0, 1))


    